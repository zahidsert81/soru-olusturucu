import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Image processing utilities"""

    @staticmethod
    def preprocess_image(image_path: str) -> np.ndarray:
        """
        Preprocess image for OCR
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Cannot read image: {image_path}")

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply bilateral filter to reduce noise while keeping edges sharp
            filtered = cv2.bilateralFilter(gray, 9, 75, 75)

            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(filtered)

            # Apply threshold
            _, thresh = cv2.threshold(enhanced, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Apply morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            return morph

        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise

    @staticmethod
    def deskew_image(image: np.ndarray) -> np.ndarray:
        """
        Deskew image if text is rotated
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Deskewed image
        """
        try:
            coords = np.column_stack(np.where(image > 0))
            angle = cv2.minAreaRect(coords)[2]

            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_WHITE)

            return rotated

        except Exception as e:
            logger.error(f"Error deskewing image: {e}")
            return image

    @staticmethod
    def resize_image(image: np.ndarray, scale: float = 2.0) -> np.ndarray:
        """
        Resize image for better OCR results
        
        Args:
            image: Input image
            scale: Scale factor
            
        Returns:
            Resized image
        """
        try:
            height, width = image.shape[:2]
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            return resized
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return image

    @staticmethod
    def extract_text_regions(image: np.ndarray) -> list:
        """
        Extract text regions from image
        
        Args:
            image: Input image
            
        Returns:
            List of text region bounding boxes
        """
        try:
            # Find contours
            contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # Filter small regions
                if w > 30 and h > 10:
                    regions.append({"x": x, "y": y, "w": w, "h": h, "area": w * h})
            
            # Sort by y coordinate (top to bottom)
            regions.sort(key=lambda r: r["y"])
            
            return regions

        except Exception as e:
            logger.error(f"Error extracting text regions: {e}")
            return []
