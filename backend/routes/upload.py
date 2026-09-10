from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/upload", tags=["upload"])

UPLOAD_DIR = Path("uploads/pdfs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    PDF dosyası yükle
    """
    try:
        # Dosya türünü kontrol et
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Sadece PDF dosyaları kabul edilir")
        
        # Dosya boyutunu kontrol et (max 50MB)
        content = await file.read()
        if len(content) > 50 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Dosya çok büyük (max 50MB)")
        
        # Unique dosya adı oluştur
        file_extension = ".pdf"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Dosyayı kaydet
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "status": "success",
            "message": "PDF başarıyla yüklendi",
            "file_id": unique_filename.replace(".pdf", ""),
            "filename": file.filename,
            "size": len(content),
            "uploaded_at": datetime.now().isoformat()
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yükleme hatası: {str(e)}")

@router.get("/status/{file_id}")
async def check_upload_status(file_id: str):
    """
    Yüklenmiş dosyanın durumunu kontrol et
    """
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")
    
    return {
        "file_id": file_id,
        "exists": True,
        "size": file_path.stat().st_size,
        "uploaded_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
    }
