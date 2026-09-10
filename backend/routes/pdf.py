from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import logging
import os

from database import get_db
from models.question import PDFDocument, Question, OCRResult
from models.schemas import (
    QuestionResponse, PDFProcessingStatusResponse,
    QuestionsExportRequest
)
from processors import PDFProcessor, OCRProcessor, QuestionDetector, ImageProcessor

router = APIRouter(prefix="/api/pdf", tags=["pdf"])
logger = logging.getLogger(__name__)


@router.post("/process/{pdf_id}")
async def process_pdf(
    pdf_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start PDF processing in background
    
    Args:
        pdf_id: PDF ID to process
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Processing started response
    """
    try:
        pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()
        
        if not pdf_doc:
            raise HTTPException(status_code=404, detail="PDF not found")

        if not os.path.exists(pdf_doc.file_path):
            raise HTTPException(status_code=404, detail="PDF file not found on disk")

        # Update status
        pdf_doc.status = "processing"
        db.commit()

        # Add background task
        background_tasks.add_task(_process_pdf_background, pdf_id, pdf_doc.file_path, db)

        return {
            "message": "PDF processing started",
            "pdf_id": pdf_id,
            "status": "processing"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting PDF processing: {e}")
        raise HTTPException(status_code=500, detail="Error starting PDF processing")


async def _process_pdf_background(pdf_id: int, file_path: str, db: Session):
    """Background task to process PDF"""
    try:
        pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()
        
        # Extract text from PDF
        text_dict = PDFProcessor.extract_text_from_pdf(file_path)
        
        ocr_processor = OCRProcessor()
        question_detector = QuestionDetector()
        
        # Process each page
        for page_num, text in text_dict.items():
            if text.strip():
                # Save OCR result
                ocr_result = OCRResult(
                    pdf_id=pdf_id,
                    page_number=page_num,
                    extracted_text=text
                )
                db.add(ocr_result)
                
                # Detect questions
                questions = question_detector.detect_questions(text)
                
                for q_data in questions:
                    if question_detector.validate_question(q_data):
                        # Classify question
                        classification = question_detector.classify_question(
                            q_data.get("question", ""),
                            q_data.get("options", [])
                        )
                        
                        question = Question(
                            pdf_id=pdf_id,
                            question_text=q_data.get("question", ""),
                            question_type=classification.get("type", "unknown"),
                            options=str(q_data.get("options", [])),
                            source_page=page_num
                        )
                        db.add(question)

        db.commit()
        
        # Update PDF status
        pdf_doc.status = "completed"
        db.commit()
        
        logger.info(f"PDF {pdf_id} processed successfully")

    except Exception as e:
        logger.error(f"Error processing PDF {pdf_id}: {e}")
        pdf_doc.status = "failed"
        pdf_doc.error_message = str(e)
        db.commit()


@router.get("/status/{pdf_id}", response_model=PDFProcessingStatusResponse)
async def get_processing_status(pdf_id: int, db: Session = Depends(get_db)):
    """
    Get PDF processing status
    
    Args:
        pdf_id: PDF ID
        db: Database session
        
    Returns:
        Processing status
    """
    try:
        pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()
        
        if not pdf_doc:
            raise HTTPException(status_code=404, detail="PDF not found")

        # Count extracted questions
        questions_count = db.query(Question).filter(Question.pdf_id == pdf_id).count()

        return PDFProcessingStatusResponse(
            pdf_id=pdf_id,
            status=pdf_doc.status,
            num_pages=pdf_doc.num_pages,
            questions_count=questions_count,
            error_message=pdf_doc.error_message
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting processing status: {e}")
        raise HTTPException(status_code=500, detail="Error getting processing status")


@router.get("/text/{pdf_id}")
async def get_extracted_text(pdf_id: int, db: Session = Depends(get_db)):
    """
    Get extracted text from PDF
    
    Args:
        pdf_id: PDF ID
        db: Database session
        
    Returns:
        Extracted text by page
    """
    try:
        ocr_results = db.query(OCRResult).filter(OCRResult.pdf_id == pdf_id).all()
        
        if not ocr_results:
            raise HTTPException(status_code=404, detail="No extracted text found")

        text_by_page = {
            result.page_number: result.extracted_text
            for result in ocr_results
        }

        return {
            "pdf_id": pdf_id,
            "text_by_page": text_by_page
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting extracted text: {e}")
        raise HTTPException(status_code=500, detail="Error getting extracted text")
