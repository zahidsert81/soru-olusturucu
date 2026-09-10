from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/api/questions", tags=["questions"])

QUESTIONS_DB = Path("data/questions.json")

def load_questions() -> List[dict]:
    """
    Sorular veritabanından yükle
    """
    if QUESTIONS_DB.exists():
        with open(QUESTIONS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_questions(questions: List[dict]):
    """
    Soruları veritabanına kaydet
    """
    QUESTIONS_DB.parent.mkdir(parents=True, exist_ok=True)
    with open(QUESTIONS_DB, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

@router.get("/")
async def get_questions(
    difficulty: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Soruları listele (filtreleme ile)
    """
    try:
        questions = load_questions()
        
        # Filtreleme
        if difficulty:
            questions = [q for q in questions if q.get('difficulty') == difficulty]
        
        if subject:
            questions = [q for q in questions if q.get('subject') == subject]
        
        # Sınırlandırma
        questions = questions[:limit]
        
        return {
            "status": "success",
            "count": len(questions),
            "questions": questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{question_id}")
async def get_question(question_id: int):
    """
    Tek bir soruyu getir
    """
    try:
        questions = load_questions()
        question = next((q for q in questions if q.get('id') == question_id), None)
        
        if not question:
            raise HTTPException(status_code=404, detail="Soru bulunamadı")
        
        return {
            "status": "success",
            "question": question
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
async def create_question(question_data: dict):
    """
    Yeni soru oluştur
    """
    try:
        questions = load_questions()
        
        # ID oluştur
        new_id = max([q.get('id', 0) for q in questions] or [0]) + 1
        
        new_question = {
            "id": new_id,
            "number": question_data.get('number'),
            "text": question_data.get('text'),
            "options": question_data.get('options', []),
            "difficulty": question_data.get('difficulty', 'Orta'),
            "subject": question_data.get('subject', 'Matematik'),
            "image_path": question_data.get('image_path'),
            "has_image": question_data.get('has_image', False),
            "created_at": datetime.now().isoformat()
        }
        
        questions.append(new_question)
        save_questions(questions)
        
        return {
            "status": "success",
            "message": "Soru başarıyla oluşturuldu",
            "question": new_question
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_statistics():
    """
    Soru istatistikleri
    """
    try:
        questions = load_questions()
        
        difficulties = {}
        subjects = {}
        
        for q in questions:
            diff = q.get('difficulty', 'Bilinmiyor')
            subj = q.get('subject', 'Bilinmiyor')
            
            difficulties[diff] = difficulties.get(diff, 0) + 1
            subjects[subj] = subjects.get(subj, 0) + 1
        
        return {
            "status": "success",
            "total_questions": len(questions),
            "by_difficulty": difficulties,
            "by_subject": subjects
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
