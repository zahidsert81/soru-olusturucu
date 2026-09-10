import pytesseract
from paddleocr import PaddleOCR
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class OCRProcessor:
    """OCR processing using Tesseract and PaddleOCR"""

    def __init__(self):
        """Initialize OCR engines"""
        try:
            self.paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.warning(f"PaddleOCR initialization failed: {e}")
            self.paddle_ocr = None

    def extract_text_tesseract(self, image, lang: str = "eng") -> str:
        """
        Extract text using Tesseract
        
        Args:
            image: Image as numpy array or PIL Image
            lang: Language code
            
        Returns:
            Extracted text
        """
        try:
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {e}")
            return ""

    def extract_text_paddle(self, image) -> Tuple[str, float]:
        """
        Extract text using PaddleOCR
        
        Args:
            image: Image as numpy array
            
        Returns:
            Tuple of (extracted text, average confidence)
        """
        try:
            if self.paddle_ocr is None:
                return "", 0.0

            result = self.paddle_ocr.ocr(image, cls=True)
            
            if not result or not result[0]:
                return "", 0.0

            texts = []
            confidences = []
            
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                texts.append(text)
                confidences.append(confidence)

            full_text = " ".join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return full_text.strip(), avg_confidence

        except Exception as e:
            logger.error(f"PaddleOCR failed: {e}")
            return "", 0.0

    def extract_text_hybrid(self, image) -> str:
        """
        Extract text using both engines and combine results
        
        Args:
            image: Image as numpy array
            
        Returns:
            Extracted text
        """
        try:
            # Try PaddleOCR first
            paddle_text, confidence = self.extract_text_paddle(image)
            
            if confidence > 0.7:  # High confidence from PaddleOCR
                return paddle_text
            
            # Fallback to Tesseract
            tesseract_text = self.extract_text_tesseract(image)
            
            # Use PaddleOCR if it has some text
            if paddle_text and confidence > 0.4:
                return paddle_text
            
            return tesseract_text

        except Exception as e:
            logger.error(f"Hybrid OCR failed: {e}")
            return ""

    def get_detailed_results(self, image) -> dict:
        """
        Get detailed OCR results with confidence scores
        
        Args:
            image: Image as numpy array
            
        Returns:
            Dictionary with OCR results
        """
        try:
            paddle_text, paddle_conf = self.extract_text_paddle(image)
            tesseract_text = self.extract_text_tesseract(image)
            
            return {
                "paddle_ocr": {
                    "text": paddle_text,
                    "confidence": paddle_conf
                },
                "tesseract_ocr": {
                    "text": tesseract_text
                },
                "final_text": paddle_text if paddle_text else tesseract_text,
                "method": "paddle" if paddle_text else "tesseract"
            }

        except Exception as e:
            logger.error(f"Error getting detailed OCR results: {e}")
            return {
                "error": str(e),
                "final_text": ""
            }
