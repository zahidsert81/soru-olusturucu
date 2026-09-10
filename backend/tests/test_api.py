import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
import sys

# Backend'i import et
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
from app import app

client = TestClient(app)

class TestHealthEndpoints:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_info_endpoint(self):
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "api_name" in data
        assert "version" in data
        assert "features" in data

class TestQuestionsEndpoints:
    def test_get_empty_questions(self):
        response = client.get("/api/questions/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "questions" in data
        assert "count" in data

    def test_create_question(self):
        question_data = {
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
        }
        
        response = client.post("/api/questions/create", json=question_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "question" in data

    def test_get_questions_with_filters(self):
        response = client.get("/api/questions/?difficulty=Kolay&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_statistics(self):
        response = client.get("/api/questions/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_questions" in data
        assert "by_difficulty" in data
        assert "by_subject" in data

class TestUploadEndpoints:
    def test_invalid_file_type(self, tmp_path):
        # Non-PDF dosya oluştur
        fake_file = tmp_path / "test.txt"
        fake_file.write_text("test")
        
        with open(fake_file, "rb") as f:
            response = client.post(
                "/api/upload/pdf",
                files={"file": ("test.txt", f, "text/plain")}
            )
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data

class TestPDFEndpoints:
    def test_generate_pdf_no_questions(self):
        response = client.post("/api/pdf/generate")
        # Henüz soru olmadığından error dönmeli
        assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
