# Генерация SSL сертификатов для HTTPS
Write-Host "🔐 Генерация SSL сертификатов для HTTPS..." -ForegroundColor Green

# Создаем директорию для сертификатов
if (!(Test-Path "ssl")) {
    New-Item -ItemType Directory -Path "ssl"
    Write-Host "✅ Создана директория ssl" -ForegroundColor Green
}

# Проверяем наличие OpenSSL
try {
    $opensslVersion = openssl version
    Write-Host "✅ OpenSSL найден: $opensslVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ OpenSSL не найден. Установите OpenSSL для Windows" -ForegroundColor Red
    Write-Host "Скачать можно с: https://slproweb.com/products/Win32OpenSSL.html" -ForegroundColor Yellow
    exit 1
}

# Генерируем самоподписанный сертификат
Write-Host "🔐 Генерация сертификата..." -ForegroundColor Yellow

openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
    -keyout ssl/key.pem `
    -out ssl/cert.pem `
    -subj "/C=RU/ST=Moscow/L=Moscow/O=NoaMetrics/OU=Development/CN=localhost"

# Проверяем создание файлов
if ((Test-Path "ssl/cert.pem") -and (Test-Path "ssl/key.pem")) {
    Write-Host "✅ SSL сертификаты созданы:" -ForegroundColor Green
    Write-Host "   - ssl/cert.pem (сертификат)" -ForegroundColor Cyan
    Write-Host "   - ssl/key.pem (приватный ключ)" -ForegroundColor Cyan
    Write-Host "🔐 Теперь можно запускать с HTTPS" -ForegroundColor Green
} else {
    Write-Host "❌ Ошибка создания сертификатов" -ForegroundColor Red
    exit 1
} 