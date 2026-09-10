import pytest
from pathlib import Path
import sys

# Backend'i import et
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
from processors.question_detector import QuestionDetector

class TestQuestionDetector:
    def setup_method(self):
        self.detector = QuestionDetector()

    def test_parse_question_text(self):
        text = """1. 2 + 2 = ?
        A) 3
        B) 4
        C) 5
        D) 6
        """
        
        result = self.detector.parse_question_text(text)
        assert result["number"] == 1
        assert result["text"] == "2 + 2 = ?"
        assert len(result["options"]) == 4
        assert result["options"][0]["letter"] == "A"

    def test_validate_valid_question(self):
        question = {
            "text": "Test sorusu",
            "options": [
                {"letter": "A", "text": "Seçenek A"},
                {"letter": "B", "text": "Seçenek B"}
            ]
        }
        assert self.detector.validate_question(question) is True

    def test_validate_invalid_question_no_options(self):
        question = {
            "text": "Test sorusu",
            "options": []
        }
        assert self.detector.validate_question(question) is False

    def test_validate_invalid_question_no_text(self):
        question = {
            "text": "",
            "options": [
                {"letter": "A", "text": "Seçenek A"},
                {"letter": "B", "text": "Seçenek B"}
            ]
        }
        assert self.detector.validate_question(question) is False

    def test_format_question(self):
        question_data = {
            "number": 1,
            "text": "Test sorusu",
            "options": [
                {"letter": "A", "text": "Seçenek A"},
                {"letter": "B", "text": "Seçenek B"}
            ]
        }
        
        formatted = self.detector.format_question(question_data, "Zor")
        assert formatted["number"] == 1
        assert formatted["difficulty"] == "Zor"
        assert formatted["subject"] == "Matematik"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
