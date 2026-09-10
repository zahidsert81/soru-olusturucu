import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class QuestionDetector:
    """Detect and extract questions from text"""

    # Common question patterns
    QUESTION_PATTERNS = [
        r'^\s*\d+[\.\)]\s*(.+?)\?',  # "1. Question?" or "1) Question?"
        r'^\s*[A-Z]\)?\s*(.+?)\?',   # "A) Question?" 
        r'^\s*\*+\s*(.+?)\?',        # "*** Question?"
        r'Question\s*\d+[\.\)]\s*(.+?)\?',  # "Question 1. ..."
    ]

    MULTIPLE_CHOICE_OPTIONS = re.compile(
        r'^[a-dA-D][\.\)]\s*(.+)$|'  # a) option or a. option
        r'^[①②③④](.+)$|'              # circled numbers
        r'^\([a-dA-D]\)\s*(.+)$',     # (a) option
        re.MULTILINE
    )

    @staticmethod
    def detect_questions(text: str) -> List[Dict]:
        """
        Detect questions in text
        
        Args:
            text: Input text
            
        Returns:
            List of detected questions with metadata
        """
        questions = []
        lines = text.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue

            # Check if line contains a question
            is_question = QuestionDetector._is_question_line(line)
            
            if is_question:
                question_data = {
                    "question": line,
                    "type": "unknown",
                    "options": [],
                    "line_number": i
                }

                # Look ahead for options
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    
                    if not next_line:
                        i += 1
                        continue

                    if QuestionDetector.MULTIPLE_CHOICE_OPTIONS.match(next_line):
                        question_data["options"].append(next_line)
                        question_data["type"] = "multiple_choice"
                        i += 1
                    elif QuestionDetector._is_question_line(next_line):
                        # Next question found
                        break
                    else:
                        i += 1

                if question_data["question"]:
                    questions.append(question_data)
            else:
                i += 1

        return questions

    @staticmethod
    def _is_question_line(line: str) -> bool:
        """
        Check if a line is likely a question
        
        Args:
            line: Input line
            
        Returns:
            True if line appears to be a question
        """
        line = line.strip()
        
        # Must end with question mark
        if not line.endswith('?'):
            return False

        # Must not start with common non-question patterns
        non_question_starts = ['http', 'www', 'email', '@', 'Phone', 'Tel']
        if any(line.lower().startswith(pattern.lower()) for pattern in non_question_starts):
            return False

        # Minimum length
        if len(line) < 10:
            return False

        return True

    @staticmethod
    def classify_question(question_text: str, options: List[str]) -> Dict:
        """
        Classify question type
        
        Args:
            question_text: Question text
            options: List of options
            
        Returns:
            Classification result
        """
        classification = {
            "type": "short_answer",
            "confidence": 0.5,
            "details": {}
        }

        if options:
            if len(options) == 2 and any(keyword in opt.lower() for opt in options 
                                        for keyword in ['true', 'false', 'evet', 'hayir']):
                classification["type"] = "true_false"
                classification["confidence"] = 0.95
            elif 2 <= len(options) <= 5:
                classification["type"] = "multiple_choice"
                classification["confidence"] = 0.90
            
            classification["details"]["options_count"] = len(options)

        # Check for specific patterns
        if any(keyword in question_text.lower() for keyword in ['kaç', 'ne kadar', 'how many', 'how much']):
            classification["type"] = "numerical"
        elif any(keyword in question_text.lower() for keyword in ['açıkla', 'explain', 'neden', 'why']):
            classification["type"] = "essay"

        return classification

    @staticmethod
    def extract_answer_key(text: str) -> Dict[int, str]:
        """
        Extract answer key from text
        
        Args:
            text: Input text (often from end of document)
            
        Returns:
            Dictionary mapping question number to answer
        """
        answer_key = {}
        
        # Patterns for answer keys
        patterns = [
            r'(?:Answer|Cevap|Key|Anahtar)\s*[\:\s]*\s*(?:Key|Tuşu)?.*?\n(.*?)(?:\n\n|$)',
            r'(?:Answers|Cevaplar)[\:\s]*\n(.*?)(?:\n\n|$)',
        ]

        try:
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                for match in matches:
                    answer_section = match.group(1)
                    lines = answer_section.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        # Try to parse "1. A" or "1) B" format
                        match_ans = re.match(r'(\d+)[\.\)]\s*([A-Za-z0-9])', line)
                        if match_ans:
                            q_num = int(match_ans.group(1))
                            answer = match_ans.group(2).upper()
                            answer_key[q_num] = answer

        except Exception as e:
            logger.error(f"Error extracting answer key: {e}")

        return answer_key

    @staticmethod
    def validate_question(question_data: Dict) -> bool:
        """
        Validate if extracted data is a valid question
        
        Args:
            question_data: Question data to validate
            
        Returns:
            True if valid question
        """
        required_fields = ["question"]
        
        if not all(field in question_data for field in required_fields):
            return False

        question = question_data.get("question", "").strip()
        
        # Minimum length
        if len(question) < 10:
            return False

        # Must contain question mark
        if '?' not in question:
            return False

        return True
