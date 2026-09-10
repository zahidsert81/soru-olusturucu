# 🤝 Katkıda Bulunma Rehberi

## Başlamadan Önce

1. Repository'yi fork edin
2. Feature branch'i oluşturun: `git checkout -b feature/amazing-feature`
3. Değişiklikleri commit edin: `git commit -m 'Add amazing feature'`
4. Branch'i push edin: `git push origin feature/amazing-feature`
5. Pull Request açın

## Coding Standards

### Python
- PEP 8'i takip edin
- Type hints kullanın
- Docstring ekleyin
```python
def process_pdf(pdf_path: str) -> List[np.ndarray]:
    """
    PDF dosyasını görsellere dönüştür
    
    Args:
        pdf_path: PDF dosyasının yolu
    
    Returns:
        Sayfa görselleri listesi
    """
    pass
```

### React/JavaScript
- ES6+ syntax kullanın
- Functional components tercih edin
- Props validation yapın
```javascript
const FileUpload = ({ onUpload, maxSize = 50 }) => {
  // Component code
}
```

## Commit Messages

Shakespeare Convention kullanın:
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: Yeni feature
- `fix`: Bug fix
- `docs`: Dokumentasyon
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Dependencies, build

**Örnekler:**
```
feat: PDF processing algorithm optimization

Improved performance by 40% using vectorized operations

Closes #123
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. README'yi güncelleyin
2. Tests ekleyin
3. Tüm tests geçtiğini doğrulayın
4. PR açıklarken değişikliklerinizi açıklayın

## Issues

- Bug report: Reproducer adımları ekleyin
- Feature request: Neden gerekli olduğunu açıklayın
- Documentation: Hangi kısımda sorun yaşadığınızı yazın

## Lisans

Projeyi fork etmek, bu projenin MIT Lisansı'na uyduğunuz anlamına gelir.
