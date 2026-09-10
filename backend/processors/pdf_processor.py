import PyPDF2
import os
from pathlib import Path
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)


class PDFProcessor:
    """PDF processing and extraction"""

    @staticmethod
    def get_pdf_info(pdf_path: str) -> dict:
        """
        Get PDF information
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with PDF info
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Get metadata
                metadata = pdf_reader.metadata
                
                return {
                    "num_pages": num_pages,
                    "title": metadata.title if metadata else None,
                    "author": metadata.author if metadata else None,
                    "subject": metadata.subject if metadata else None,
                    "creator": metadata.creator if metadata else None
                }

        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            raise

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> dict:
        """
        Extract text from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text per page
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                extracted_text = {}
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        extracted_text[page_num] = text
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")
                        extracted_text[page_num] = ""
                
                return extracted_text

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    @staticmethod
    def convert_pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> list:
        """
        Convert PDF pages to images
        
        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save images
            dpi: DPI for conversion
            
        Returns:
            List of generated image paths
        """
        try:
            # Try using fitz (PyMuPDF) first
            try:
                import fitz
                doc = fitz.open(pdf_path)
                image_paths = []
                
                os.makedirs(output_dir, exist_ok=True)
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    # Render page to image
                    pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                    
                    image_path = os.path.join(output_dir, f"page_{page_num:03d}.png")
                    pix.save(image_path)
                    image_paths.append(image_path)
                
                doc.close()
                return image_paths
                
            except ImportError:
                logger.warning("fitz not available, using PyPDF2 fallback")
                # Fallback: return info about what would need to be done
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    logger.info(f"PDF has {num_pages} pages. Please install 'PyMuPDF' for image conversion.")
                    return []

        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            raise

    @staticmethod
    def split_pdf(pdf_path: str, start_page: int, end_page: int, output_path: str) -> bool:
        """
        Split PDF by page range
        
        Args:
            pdf_path: Path to input PDF
            start_page: Start page number (0-indexed)
            end_page: End page number (0-indexed, inclusive)
            output_path: Path to output PDF
            
        Returns:
            True if successful
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                for page_num in range(start_page, min(end_page + 1, len(pdf_reader.pages))):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                return True

        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            return False

    @staticmethod
    def merge_pdfs(pdf_paths: list, output_path: str) -> bool:
        """
        Merge multiple PDFs
        
        Args:
            pdf_paths: List of PDF file paths
            output_path: Path to output merged PDF
            
        Returns:
            True if successful
        """
        try:
            pdf_writer = PyPDF2.PdfWriter()
            
            for pdf_path in pdf_paths:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True

        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return False
