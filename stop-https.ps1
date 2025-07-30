# Остановка приложения с HTTPS
Write-Host "🛑 Остановка NoaMetrics с HTTPS..." -ForegroundColor Yellow

# Останавливаем контейнеры
docker-compose -f docker-compose.https.yml down

Write-Host "✅ Приложение остановлено!" -ForegroundColor Green 