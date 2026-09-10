# 🔐 Güvenlik Politikası

## Güvenlik Açığı Bildirimi

Güvenlik açığı bulduysanız, lütfen **public** olarak bildirmeyin.

**Contact:** sertmzahid@gmail.com

**Format:**
- Açığın açıklaması
- Etkilenen bileşenler
- Olası etki
- Öneri edilen fix (opsiyonel)

## Güvenlik Önlemleri

### Backend
- ✅ CORS konfigürasyonu
- ✅ File upload validation
- ✅ Size limitations (50MB max)
- ✅ File type checking
- ✅ Input sanitization
- ⚠️ TODO: Authentication/Authorization
- ⚠️ TODO: Rate limiting
- ⚠️ TODO: SQL injection prevention

### Frontend
- ✅ XSS prevention
- ✅ CSRF protection
- ⚠️ TODO: Content Security Policy
- ⚠️ TODO: Secure headers

## Best Practices

1. **Environment Variables**
   ```bash
   # .env dosyası oluşturun
   FASTAPI_ENV=production
   DEBUG=False
   ```

2. **File Upload**
   - Dosya türü kontrol edin
   - Dosya boyutunu sınırlayın
   - Virus scan yapın (production)

3. **Database**
   - Parameterized queries kullanın
   - Backup alın

4. **Deployment**
   - HTTPS kullanın
   - Firewall konfigürasyonu
   - Regular updates

## Known Issues

- OCR kullanırken PaddleOCR yüklemesi zaman alabilir
- Large PDFs (50MB+) processing timeout'a neden olabilir

## Roadmap

- [ ] User authentication
- [ ] Role-based access control
- [ ] Encrypted file storage
- [ ] Audit logging
- [ ] 2FA support
