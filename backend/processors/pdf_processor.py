import pdfplumber
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
import tempfile
from PIL import Image

class PDFProcessor:
    """
    PDF dosyalarını işleyerek görsellere dönüştüren sınıf
    """
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.images = []
    
    def extract_images(self) -> List[np.ndarray]:
        """
        PDF'den tüm sayfaları görsellere dönüştür
        """
        images = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Sayfayı görüntüye dönüştür (DPI: 300)
                    pil_image = page.to_image(resolution=300).original
                    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                    images.append(image)
            
            self.images = images
            return images
        except Exception as e:
            print(f"PDF işleme hatası: {e}")
            return []
    
    def get_page_count(self) -> int:
        """
        PDF'deki sayfa sayısını döndür
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            print(f"Sayfa sayısı alma hatası: {e}")
            return 0
    
    def extract_text(self) -> List[str]:
        """
        PDF'den metni çıkar
        """
        texts = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    texts.append(text if text else "")
            return texts
        except Exception as e:
            print(f"Metin çıkarma hatası: {e}")
            return []
