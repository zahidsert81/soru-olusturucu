# 📚 API Belgeleri

## Genel Bilgi

**Base URL:** `http://localhost:8000/api`

**Authentication:** Şu anda kimlik doğrulaması gerekli değildir.

## Upload Endpoints

### PDF Yükleme
```http
POST /upload/pdf
Content-Type: multipart/form-data

Body:
- file: PDF dosyası (max 50MB)
```

**Başarılı Yanıt (200):**
```json
{
  "status": "success",
  "message": "PDF başarıyla yüklendi",
  "file_id": "abc123",
  "filename": "test.pdf",
  "size": 1024000,
  "uploaded_at": "2024-01-10T10:30:00"
}
```

### Yükleme Durumunu Kontrol Etme
```http
GET /upload/status/{file_id}
```

**Başarılı Yanıt (200):**
```json
{
  "file_id": "abc123",
  "exists": true,
  "size": 1024000,
  "uploaded_at": "2024-01-10T10:30:00"
}
```

## Question Endpoints

### Sorular Listesi
```http
GET /questions/?difficulty=Orta&subject=Matematik&limit=100
```

**Başarılı Yanıt (200):**
```json
{
  "status": "success",
  "count": 10,
  "questions": [
    {
      "id": 1,
      "number": 1,
      "text": "2 + 2 = ?",
      "options": [
        {"letter": "A", "text": "3"},
        {"letter": "B", "text": "4"},
        {"letter": "C", "text": "5"},
        {"letter": "D", "text": "6"}
      ],
      "difficulty": "Kolay",
      "subject": "Matematik",
      "image_path": null,
      "has_image": false
    }
  ]
}
```

### Tek Soru Getirme
```http
GET /questions/{question_id}
```

### Yeni Soru Oluşturma
```http
POST /questions/create
Content-Type: application/json

Body:
{
  "number": 1,
  "text": "Soru metni",
  "options": [
    {"letter": "A", "text": "Seçenek A"},
    {"letter": "B", "text": "Seçenek B"},
    {"letter": "C", "text": "Seçenek C"},
    {"letter": "D", "text": "Seçenek D"}
  ],
  "difficulty": "Orta",
  "subject": "Matematik"
}
```

### İstatistikler
```http
GET /questions/stats/summary
```

**Başarılı Yanıt (200):**
```json
{
  "status": "success",
  "total_questions": 50,
  "by_difficulty": {
    "Kolay": 10,
    "Orta": 30,
    "Zor": 10
  },
  "by_subject": {
    "Matematik": 20,
    "Türkçe": 15,
    "Fen": 15
  }
}
```

## PDF Endpoints

### PDF Oluşturma
```http
POST /pdf/generate
```

**Başarılı Yanıt (200):**
```json
{
  "status": "success",
  "message": "PDF başarıyla oluşturuldu",
  "filename": "soru_bankasi_20240110_103000.pdf",
  "total_questions": 50,
  "file_size": 512000,
  "download_url": "/api/pdf/download/soru_bankasi_20240110_103000.pdf"
}
```

### PDF İndirme
```http
GET /pdf/download/{filename}
```

## Hata Yanıtları

### 400 - Bad Request
```json
{
  "detail": "Sadece PDF dosyaları kabul edilir"
}
```

### 404 - Not Found
```json
{
  "detail": "Dosya bulunamadı"
}
```

### 413 - Payload Too Large
```json
{
  "detail": "Dosya çok büyük (max 50MB)"
}
```

### 500 - Internal Server Error
```json
{
  "detail": "Sunucu hatası: ..."
}
```

## Örnek Requests

### cURL

**PDF Yükleme:**
```bash
curl -X POST http://localhost:8000/api/upload/pdf \
  -F "file=@test.pdf"
```

**Sorular Listesi:**
```bash
curl http://localhost:8000/api/questions/?limit=10
```

**Yeni Soru Oluşturma:**
```bash
curl -X POST http://localhost:8000/api/questions/create \
  -H "Content-Type: application/json" \
  -d '{
    "number": 1,
    "text": "2 + 2 = ?",
    "options": [
      {"letter": "A", "text": "3"},
      {"letter": "B", "text": "4"},
      {"letter": "C", "text": "5"},
      {"letter": "D", "text": "6"}
    ],
    "difficulty": "Kolay",
    "subject": "Matematik"
  }'
```

**PDF Oluşturma:**
```bash
curl -X POST http://localhost:8000/api/pdf/generate
```

### Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# PDF Yükleme
with open('test.pdf', 'rb') as f:
    response = requests.post(
        f"{BASE_URL}/upload/pdf",
        files={'file': f}
    )
    print(response.json())

# Sorular Listesi
response = requests.get(f"{BASE_URL}/questions/")
questions = response.json()

# PDF Oluşturma
response = requests.post(f"{BASE_URL}/pdf/generate")
pdf_data = response.json()
```

## Rate Limiting

Şu anda rate limiting aktif değildir.

## Versioning

API versiyonu: `1.0.0`

Future versions için: `/api/v2/..`
