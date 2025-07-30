# Запуск приложения с HTTPS
Write-Host "🚀 Запуск NoaMetrics с HTTPS..." -ForegroundColor Green

# Проверяем наличие SSL сертификатов
if (!(Test-Path "ssl/cert.pem") -or !(Test-Path "ssl/key.pem")) {
    Write-Host "❌ SSL сертификаты не найдены!" -ForegroundColor Red
    Write-Host "🔐 Генерируем SSL сертификаты..." -ForegroundColor Yellow
    
    # Запускаем генерацию сертификатов
    if (Test-Path "generate-ssl-cert.ps1") {
        & .\generate-ssl-cert.ps1
    } else {
        Write-Host "❌ Скрипт generate-ssl-cert.ps1 не найден!" -ForegroundColor Red
        exit 1
    }
}

# Останавливаем существующие контейнеры
Write-Host "🛑 Останавливаем существующие контейнеры..." -ForegroundColor Yellow
docker-compose down

# Запускаем с HTTPS конфигурацией
Write-Host "🚀 Запускаем приложение с HTTPS..." -ForegroundColor Green
docker-compose -f docker-compose.https.yml up -d

# Ждем запуска сервисов
Write-Host "⏳ Ждем запуска сервисов..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Проверяем статус
Write-Host "📊 Проверяем статус сервисов..." -ForegroundColor Yellow
docker-compose -f docker-compose.https.yml ps

Write-Host "✅ Приложение запущено с HTTPS!" -ForegroundColor Green
Write-Host "🌐 Откройте в браузере:" -ForegroundColor Cyan
Write-Host "   https://localhost" -ForegroundColor White
Write-Host "   https://localhost:443" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Примечание: Браузер может показать предупреждение о самоподписанном сертификате." -ForegroundColor Yellow
Write-Host "   Нажмите 'Дополнительно' -> 'Перейти на localhost (небезопасно)'" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔧 Для доступа с других устройств используйте IP адрес вашего компьютера:" -ForegroundColor Cyan
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
if ($ipAddress) {
    Write-Host "   https://$ipAddress" -ForegroundColor White
} else {
    Write-Host "   IP адрес не найден" -ForegroundColor Red
} 