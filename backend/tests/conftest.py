# Backend Tests Konfigürasyonu
import sys
from pathlib import Path

# Backend modüllerini import yoluna ekle
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

pytest_plugins = []
