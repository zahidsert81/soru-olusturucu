import cv2
import numpy as np
from typing import List, Tuple

class ImageProcessor:
    """
    Görüntüleri işleyen ve soruları algılayan sınıf
    """
    
    def __init__(self, image: np.ndarray):
        self.original_image = image.copy()
        self.image = image.copy()
    
    def detect_contours(self) -> List[Tuple]:
        """
        Görüntüdeki ana konturları algıla (soru blokları)
        """
        # Gri tonlamaya dönüştür
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # İkili görüntüye dönüştür
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Konturları bul
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Bounding rectangles
        bounding_boxes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            # Çok küçük veya çok büyük olanları filtrele
            if 10000 < area < 500000:
                x, y, w, h = cv2.boundingRect(contour)
                bounding_boxes.append((x, y, w, h))
        
        # Y koordinatına göre sırala
        bounding_boxes.sort(key=lambda b: b[1])
        return bounding_boxes
    
    def crop_question(self, x: int, y: int, w: int, h: int) -> np.ndarray:
        """
        Verilen koordinatlardan soru kesip çıkar
        """
        return self.original_image[y:y+h, x:x+w]
    
    def detect_options_region(self, question_image: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Soru görüntüsünde seçeneklerin bulunduğu bölgeyi tespit et
        """
        gray = cv2.cvtColor(question_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Satırları tespit et
        h, w = binary.shape
        horizontal_projection = np.sum(binary, axis=1)
        
        # Seçeneklerin başladığı yeri bul (boş alan sonrası)
        threshold = np.max(horizontal_projection) * 0.3
        option_start = 0
        for i in range(len(horizontal_projection) - 1, -1, -1):
            if horizontal_projection[i] > threshold:
                option_start = i
                break
        
        return 0, option_start, w, h - option_start
    
    def enhance_image(self) -> np.ndarray:
        """
        Görüntü kalitesini iyileştir
        """
        # Kontrast ve parlaklığı ayarla
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
