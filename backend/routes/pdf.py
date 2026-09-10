from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pathlib import Path
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors

router = APIRouter(prefix="/api/pdf", tags=["pdf"])

OUTPUT_DIR = Path("outputs")
QUESTIONS_DB = Path("data/questions.json")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_questions() -> List[dict]:
    """Sorular veritabanından yükle"""
    if QUESTIONS_DB.exists():
        with open(QUESTIONS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

class PDFGenerator:
    """
    Yayın kalitesinde PDF oluşturan sınıf
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self.filepath = OUTPUT_DIR / filename
        self.doc = SimpleDocTemplate(
            str(self.filepath),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.styles = getSampleStyleSheet()
        self.story = []
    
    def add_title(self, title: str):
        """Başlık ekle"""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        self.story.append(Paragraph(title, title_style))
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_question(self, question: dict, index: int):
        """Soru ekle"""
        # Soru başlığı
        question_text = f"<b>{index}. {question.get('text', '')}</b>"
        question_style = ParagraphStyle(
            'Question',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#000000'),
            spaceAfter=10,
            leading=14
        )
        self.story.append(Paragraph(question_text, question_style))
        
        # Seçenekler
        options = question.get('options', [])
        if options:
            option_style = ParagraphStyle(
                'Option',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#333333'),
                spaceAfter=5,
                leftIndent=1*cm,
                leading=12
            )
            
            for option in options:
                letter = option.get('letter', '?')
                text = option.get('text', '')
                option_text = f"<b>{letter})</b> {text}"
                self.story.append(Paragraph(option_text, option_style))
        
        # Zorluk seviyesi
        difficulty = question.get('difficulty', 'Orta')
        difficulty_colors = {
            'Kolay': '#28a745',
            'Orta': '#ffc107',
            'Zor': '#dc3545'
        }
        difficulty_color = difficulty_colors.get(difficulty, '#6c757d')
        
        difficulty_text = f"<i style='color:{difficulty_color}'>Zorluk: {difficulty}</i>"
        difficulty_style = ParagraphStyle(
            'Difficulty',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=15
        )
        self.story.append(Paragraph(difficulty_text, difficulty_style))
        self.story.append(Spacer(1, 0.3*cm))
    
    def add_answer_key(self, questions: List[dict]):
        """Cevap anahtarı ekle"""
        self.story.append(PageBreak())
        
        answer_title_style = ParagraphStyle(
            'AnswerTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20
        )
        self.story.append(Paragraph("<b>CEVAP ANAHTARI</b>", answer_title_style))
        
        # Cevapları tablo ile göster
        answer_data = [['Soru No', 'Cevap', 'Zorluk']]
        for i, q in enumerate(questions, 1):
            # Bu örnekte cevap her zaman 'A' olarak ayarlandı (gerçekte database'den gelecek)
            answer_data.append([str(i), 'A', q.get('difficulty', 'Orta')])
        
        answer_table = Table(answer_data, colWidths=[3*cm, 3*cm, 3*cm])
        answer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(answer_table)
    
    def generate(self, questions: List[dict], include_answer_key: bool = False):
        """PDF'yi oluştur"""
        self.add_title("Soru Bankası")
        
        for i, question in enumerate(questions, 1):
            self.add_question(question, i)
        
        if include_answer_key:
            self.add_answer_key(questions)
        
        self.doc.build(self.story)
        return str(self.filepath)

@router.post("/generate")
async def generate_pdf(background_tasks: BackgroundTasks):
    """
    Tüm soruları PDF'ye dönüştür
    """
    try:
        questions = load_questions()
        
        if not questions:
            raise HTTPException(status_code=400, detail="Henüz soru eklenmemiş")
        
        # PDF dosya adı
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"soru_bankasi_{timestamp}.pdf"
        
        # PDF oluştur
        generator = PDFGenerator(filename)
        pdf_path = generator.generate(questions, include_answer_key=True)
        
        return {
            "status": "success",
            "message": "PDF başarıyla oluşturuldu",
            "filename": filename,
            "total_questions": len(questions),
            "file_size": Path(pdf_path).stat().st_size,
            "download_url": f"/api/pdf/download/{filename}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF oluşturma hatası: {str(e)}")

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """
    PDF dosyasını indir
    """
    from fastapi.responses import FileResponse
    
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )
