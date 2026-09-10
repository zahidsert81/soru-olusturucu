# 📚 Soru Oluşturucu - Otomatik Soru Algılama ve PDF Üretimi

PDF dosyalarından soruları otomatik olarak algılayan, düzenleyen ve yayın kalitesinde PDF çıktısı üreten modern bir uygulama.

## 🎯 Özellikler

- ✅ PDF'den soru otomatik algılama (OpenCV)
- ✅ Görüntü kesme ve düzenleme
- ✅ Zorluk seviyesi seçimi
- ✅ Modern web arayüzü (React)
- ✅ Yayın kalitesinde PDF çıktı
- ✅ Veritabanında soru yönetimi
- ✅ Drag-drop dosya yükleme

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React
- **Image Processing**: OpenCV
- **PDF Processing**: pdfplumber, ReportLab
- **Database**: SQLite
- **OCR**: PaddleOCR (opsiyonel)

## 📁 Proje Yapısı

```
soru-olusturucu/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── processors/
│   │   ├── pdf_processor.py
│   │   ├── image_processor.py
│   │   └── question_detector.py
│   └── routes/
│       ├── upload.py
│       └── questions.py
├── frontend/
│   ├── package.json
│   └── src/
├── tests/
└── README.md
```

## 🚀 Başlangıç

### Backend Kurulumu
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Kurulumu
```bash
cd frontend
npm install
npm start
```

## 📖 API Endpoints

- `POST /upload` - PDF yükleme
- `GET /questions` - Soruları listeleme
- `POST /questions/generate-pdf` - PDF oluşturma

## 📝 Lisans

MIT
