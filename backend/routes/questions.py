from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
import json

from database import get_db
from models.question import Question, PDFDocument
from models.schemas import QuestionResponse

router = APIRouter(prefix="/api/questions", tags=["questions"])
logger = logging.getLogger(__name__)


@router.get("/{pdf_id}", response_model=list[QuestionResponse])
async def get_questions(
    pdf_id: int,
    question_type: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get questions from a PDF
    
    Args:
        pdf_id: PDF ID
        question_type: Filter by question type (optional)
        page: Page number for pagination
        limit: Number of questions per page
        db: Database session
        
    Returns:
        List of questions
    """
    try:
        # Check if PDF exists
        pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()
        if not pdf_doc:
            raise HTTPException(status_code=404, detail="PDF not found")

        # Build query
        query = db.query(Question).filter(Question.pdf_id == pdf_id)
        
        if question_type:
            query = query.filter(Question.question_type == question_type)

        # Get total count
        total_count = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        questions = query.offset(offset).limit(limit).all()

        return questions

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting questions: {e}")
        raise HTTPException(status_code=500, detail="Error getting questions")


@router.get("/single/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    Get a single question
    
    Args:
        question_id: Question ID
        db: Database session
        
    Returns:
        Question details
    """
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        return question

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting question: {e}")
        raise HTTPException(status_code=500, detail="Error getting question")


@router.put("/{question_id}")
async def update_question(
    question_id: int,
    updates: dict,
    db: Session = Depends(get_db)
):
    """
    Update a question
    
    Args:
        question_id: Question ID
        updates: Fields to update
        db: Database session
        
    Returns:
        Updated question
    """
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Update allowed fields
        allowed_fields = {"question_text", "question_type", "answer", "options", "difficulty"}
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(question, field, value)

        db.commit()
        db.refresh(question)

        return question

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating question: {e}")
        raise HTTPException(status_code=500, detail="Error updating question")


@router.delete("/{question_id}")
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    """
    Delete a question
    
    Args:
        question_id: Question ID
        db: Database session
        
    Returns:
        Deletion confirmation
    """
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        db.delete(question)
        db.commit()

        return {"message": "Question deleted successfully", "id": question_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting question: {e}")
        raise HTTPException(status_code=500, detail="Error deleting question")


@router.get("/statistics/{pdf_id}")
async def get_questions_statistics(pdf_id: int, db: Session = Depends(get_db)):
    """
    Get statistics about questions in a PDF
    
    Args:
        pdf_id: PDF ID
        db: Database session
        
    Returns:
        Statistics
    """
    try:
        # Check if PDF exists
        pdf_doc = db.query(PDFDocument).filter(PDFDocument.id == pdf_id).first()
        if not pdf_doc:
            raise HTTPException(status_code=404, detail="PDF not found")

        questions = db.query(Question).filter(Question.pdf_id == pdf_id).all()
        
        # Calculate statistics
        stats = {
            "total_questions": len(questions),
            "by_type": {},
            "by_difficulty": {},
            "with_options": 0,
            "with_answers": 0
        }

        for question in questions:
            # Count by type
            q_type = question.question_type
            stats["by_type"][q_type] = stats["by_type"].get(q_type, 0) + 1

            # Count by difficulty
            if question.difficulty:
                difficulty = question.difficulty
                stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1

            # Count with options
            if question.options:
                stats["with_options"] += 1

            # Count with answers
            if question.answer:
                stats["with_answers"] += 1

        return stats

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Error getting statistics")
