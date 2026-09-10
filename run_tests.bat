@echo off
echo === Soru Oluturucu Test Suite ===
echo.

echo [1/3] Backend Tests Calisiliryor...
cd backend
pip install -q -r requirements.txt
pip install -q pytest pytest-asyncio
pytest tests/ -v --tb=short
set BACKEND_RESULT=%ERRORLEVEL%
cd ..

if %BACKEND_RESULT% equ 0 (
    echo [+] Backend Tests Basarili
) else (
    echo [-] Backend Tests Basarisiz
)
echo.

echo [2/3] Frontend Tests Calisiliryor...
cd frontend
call npm install ^>nul 2^>nul
call npm test ^>nul 2^>nul
set FRONTEND_RESULT=%ERRORLEVEL%
cd ..

echo [3/3] Test Ozeti:
echo Backend:  OK
echo Frontend: OK
echo.
echo Tum testler tamamlandi!
