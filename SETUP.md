# 🚀 Kurulum ve Çalıştırma Rehberi

## Gereksinimler

- Python 3.8+
- Node.js 16+
- npm veya yarn
- Git

## Backend Kurulumu

### 1. Backend dizinine girin
```bash
cd backend
```

### 2. Virtual environment oluşturun
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Environment dosyasını ayarlayın
```bash
cp .env.example .env
# .env dosyasını ihtiyaçlarınıza göre düzenleyin
```

### 5. Backend'i çalıştırın
```bash
python app.py
```

Backend şu adreste çalışacak: `http://localhost:8000`

## Frontend Kurulumu

### 1. Frontend dizinine girin
```bash
cd frontend
```

### 2. Bağımlılıkları yükleyin
```bash
npm install
```

### 3. Development server'ı çalıştırın
```bash
npm run dev
```

Frontend şu adreste açılacak: `http://localhost:5173`

## Docker ile Çalıştırma

### Docker Compose kullanarak her ikisini de başlatın
```bash
docker-compose up
```

## API Endpoints

### Upload
- `POST /api/upload/pdf` - PDF dosyası yükleme
- `GET /api/upload/status/{file_id}` - Yükleme durumunu kontrol etme

### Questions
- `GET /api/questions/` - Sorular listesi
- `GET /api/questions/{id}` - Tek soru getirme
- `POST /api/questions/create` - Yeni soru oluşturma
- `GET /api/questions/stats/summary` - İstatistikler

### PDF
- `POST /api/pdf/generate` - PDF oluşturma
- `GET /api/pdf/download/{filename}` - PDF indirme

## Sorun Giderme

### Port Hatası
Eğer 8000 veya 5173 portları kullanımdaysa:
```bash
# Backend port değiştirme
python app.py --port 8001

# Frontend port değiştirme
npm run dev -- --port 5174
```

### OpenCV Hatası
```bash
pip install opencv-python-headless
```

### CORS Hatası
Backend'in CORS ayarlarını kontrol edin: `backend/app.py`

## İleri Kurulum

Detaylı bilgi için [DEPLOYMENT.md](./DEPLOYMENT.md) dosyasına bakın.
