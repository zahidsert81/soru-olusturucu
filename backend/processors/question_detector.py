from typing import List, Dict
import re

class QuestionDetector:
    """
    Soruları algılayan ve yapılandıran sınıf
    """
    
    def __init__(self):
        self.questions = []
    
    def parse_question_text(self, text: str) -> Dict:
        """
        OCR metinden soru yapısını ayıkla
        """
        lines = text.strip().split('\n')
        
        question_dict = {
            'number': None,
            'text': '',
            'options': [],
            'difficulty': 'Orta'
        }
        
        # Soru numarasını bul
        if lines:
            first_line = lines[0]
            number_match = re.match(r'^(\d+)\.?', first_line)
            if number_match:
                question_dict['number'] = int(number_match.group(1))
                question_dict['text'] = first_line[number_match.end():].strip()
            else:
                question_dict['text'] = first_line
        
        # Seçenekleri bul (A, B, C, D)
        option_pattern = re.compile(r'^\s*([A-D])\)\s*(.+)$', re.MULTILINE)
        for line in lines[1:]:
            match = option_pattern.match(line)
            if match:
                question_dict['options'].append({
                    'letter': match.group(1),
                    'text': match.group(2).strip()
                })
        
        return question_dict
    
    def format_question(self, question_data: Dict, difficulty: str = 'Orta') -> Dict:
        """
        Soruyu standart formata dönüştür
        """
        return {
            'number': question_data.get('number'),
            'text': question_data.get('text', ''),
            'options': question_data.get('options', []),
            'difficulty': difficulty,
            'subject': 'Matematik',
            'image_path': None,
            'has_image': False
        }
    
    def validate_question(self, question: Dict) -> bool:
        """
        Sorunun geçerliliğini kontrol et
        """
        # Minimum 2 seçenek olmalı
        if len(question.get('options', [])) < 2:
            return False
        
        # Soru metni olmalı
        if not question.get('text', '').strip():
            return False
        
        return True
