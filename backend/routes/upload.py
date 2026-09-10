from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime
import logging

from database import get_db
from models.question import PDFDocument
from models.schemas import PDFUploadResponse
from config import Config
from processors import PDFProcessor

router = APIRouter(prefix="/api/upload", tags=["upload"])
logger = logging.getLogger(__name__)


@router.post("/pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a PDF file
    
    Args:
        file: PDF file to upload
        db: Database session
        
    Returns:
        PDFUploadResponse with file info
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Validate file size
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > Config.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {Config.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )

        # Save file
        file_path = os.path.join(Config.UPLOAD_DIR, file.filename)
        
        # Handle duplicate filenames
        if os.path.exists(file_path):
            name, ext = os.path.splitext(file.filename)
            file_path = os.path.join(Config.UPLOAD_DIR, f"{name}_{datetime.now().timestamp()}{ext}")

        with open(file_path, 'wb') as f:
            f.write(contents)

        # Get PDF info
        try:
            pdf_info = PDFProcessor.get_pdf_info(file_path)
            num_pages = pdf_info.get("num_pages", 0)
        except Exception as e:
            logger.warning(f"Could not get PDF info: {e}")
            num_pages = 0

        # Save to database
        pdf_doc = PDFDocument(
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            num_pages=num_pages,
            status="uploaded"
        )
        
        db.add(pdf_doc)
        db.commit()
        db.refresh(pdf_doc)

        logger.info(f"PDF uploaded successfully: {file.filename} (ID: {pdf_doc.id})")

        return PDFUploadResponse(
            id=pdf_doc.id,
            filename=pdf_doc.filename,
            file_size=pdf_doc.file_size,
            status=pdf_doc.status,
            created_at=pdf_doc.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.get("/status/{pdf_id}")
async def get_upload_status(pdf_id: int, db: Session = Depends(get_db)):
    """
    Get upload status of a PDF
    
    Args:
        pdf_id: PDF ID
        db: Database session
        
    Returns:
        Upload status
    """
    try:
        pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()
        
        if not pdf_doc:
            raise HTTPException(status_code=404, detail="PDF not found")

        return {
            "id": pdf_doc.id,
            "filename": pdf_doc.filename,
            "status": pdf_doc.status,
            "file_size": pdf_doc.file_size,
            "num_pages": pdf_doc.num_pages,
            "created_at": pdf_doc.created_at,
            "error": pdf_doc.error_message
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting upload status: {e}")
        raise HTTPException(status_code=500, detail="Error getting upload status")
