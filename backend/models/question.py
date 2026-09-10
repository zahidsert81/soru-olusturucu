from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class PDFDocument(Base):
    """PDF Document model"""
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True)
    file_path = Column(String(512), unique=True)
    file_size = Column(Integer)
    num_pages = Column(Integer, default=0)
    status = Column(String(50), default="processing")  # processing, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Question(Base):
    """Question model"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, index=True)
    question_text = Column(Text)
    question_type = Column(String(50))  # multiple_choice, true_false, short_answer
    answer = Column(Text, nullable=True)
    options = Column(Text, nullable=True)  # JSON format
    difficulty = Column(String(20), nullable=True)  # easy, medium, hard
    source_page = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OCRResult(Base):
    """OCR processing result"""
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, index=True)
    page_number = Column(Integer)
    extracted_text = Column(Text)
    confidence = Column(Integer, nullable=True)  # 0-100
    processing_time = Column(Integer, nullable=True)  # milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
