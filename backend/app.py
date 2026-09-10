from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from routes import all_routers

app = FastAPI(
    title="Soru Oluşturucu API",
    version="1.0.0",
    description="PDF'den soruları algılayan ve yayın kalitesinde PDF üreten uygulama"
)

# CORS middleware - Frontend bağlantısı için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gerekli dizinleri oluştur
PDF_UPLOAD_DIR = Path("uploads/pdfs")
OUTPUT_DIR = Path("outputs")
DATA_DIR = Path("data")

PDF_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Routes'u ekle
for router in all_routers:
    app.include_router(router)

# Static files (output PDFs)
try:
    app.mount("/static", StaticFiles(directory="outputs"), name="static")
except Exception as e:
    print(f"Static files mount hatası: {e}")

@app.get("/")
async def root():
    return {
        "message": "Soru Oluşturucu API - Hoş geldiniz!",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/upload/pdf",
            "questions": "/api/questions",
            "pdf": "/api/pdf/generate",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/info")
async def info():
    """Sistem bilgileri"""
    return {
        "api_name": "Soru Oluşturucu",
        "version": "1.0.0",
        "features": [
            "PDF yükleme",
            "Soru algılama (OpenCV)",
            "Soru yönetimi",
            "Zorluk seviyeleri",
            "Yayın kalitesinde PDF üretimi",
            "Cevap anahtarı"
        ],
        "upload_dir": str(PDF_UPLOAD_DIR),
        "output_dir": str(OUTPUT_DIR)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
