@echo off
REM Soru Olusturucu - Windows Setup ve Run Script
REM Bu script backend'i otomatik olarak kurar ve çalıştırır

color 0A
title Soru Olusturucu - Backend Setup

echo.
echo ====================================
echo   SORU OLUSTURUCU - BACKEND SETUP
echo ====================================
echo.

REM Backend dizinine git
cd backend

REM Python'un yüklu olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python yuklu degil! Lutfen Python 3.8+ kurun.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python bulundu.
echo.

REM Virtual environment'ı kontrol et ve yoksa oluştur
if not exist "venv\" (
    echo [INFO] Virtual environment olusturuluyor...
    python -m venv venv
    echo [OK] Virtual environment olusturuldu.
) else (
    echo [OK] Virtual environment zaten var.
)

echo.
echo [INFO] Virtual environment aktivasyon...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Virtual environment aktivasyon basarisiz!
    pause
    exit /b 1
)

echo [OK] Virtual environment aktif.
echo.

REM .env dosyasını kontrol et
if not exist ".env" (
    echo [INFO] .env dosyasi olusturuluyor...
    (
        echo # Backend Environment Variables
        echo FASTAPI_ENV=development
        echo DEBUG=True
        echo DATABASE_URL=sqlite:///./soru_olusturucu.db
        echo SECRET_KEY=your-secret-key-here
        echo UPLOAD_DIR=./uploads
        echo OUTPUT_DIR=./outputs
        echo DATA_DIR=./data
    ) > .env
    echo [OK] .env dosyasi olusturuldu.
) else (
    echo [OK] .env dosyasi zaten var.
)

echo.

REM requirements.txt kontrol et
if exist "requirements.txt" (
    echo [INFO] Paketler yukleniyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [WARNING] Paket yukleme hatasi olustu, devam ediliyor...
    ) else (
        echo [OK] Paketler basariyla yuklendi.
    )
) else (
    echo [WARNING] requirements.txt bulunamadi!
    echo [INFO] Temel paketler yukleniyor...
    pip install fastapi uvicorn python-multipart pydantic sqlalchemy
)

echo.

REM Gerekli dizinleri oluştur
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "data" mkdir data

echo [OK] Gerekli dizinler olusturuldu.
echo.

REM app.py kontrol et
if not exist "app.py" (
    echo [ERROR] app.py bulunamadi!
    echo Lutfen backend dizininde app.py dosyasinin oldugunu kontrol edin.
    pause
    exit /b 1
)

echo.
echo ====================================
echo   BACKEND BASLATILIYOR...
echo ====================================
echo.
echo Tarayici sifayi acilacaktir: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Cikis icin Ctrl+C tusuna basin...
echo.

REM Backend'i çalıştır
python app.py

pause
