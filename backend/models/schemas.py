from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PDFUploadResponse(BaseModel):
    """PDF upload response"""
    id: int
    filename: str
    file_size: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    """Base question schema"""
    question_text: str
    question_type: str
    answer: Optional[str] = None
    options: Optional[str] = None
    difficulty: Optional[str] = None
    source_page: int


class QuestionCreate(QuestionBase):
    """Question creation schema"""
    pdf_id: int


class QuestionResponse(QuestionBase):
    """Question response schema"""
    id: int
    pdf_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OCRResultResponse(BaseModel):
    """OCR result response"""
    id: int
    pdf_id: int
    page_number: int
    extracted_text: str
    confidence: Optional[int]
    processing_time: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class PDFProcessingStatusResponse(BaseModel):
    """PDF processing status"""
    pdf_id: int
    status: str
    num_pages: int
    questions_count: int
    error_message: Optional[str] = None


class QuestionsExportRequest(BaseModel):
    """Request to export questions to PDF/Word"""
    pdf_id: int
    format: str = "pdf"  # pdf or docx
    include_answers: bool = True
