# 🧹 Clean and Rebuild Frontend
# Полная очистка кэша и пересборка фронтенда

Write-Host "🧹 Cleaning frontend cache and rebuilding..." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Останавливаем dev сервер если запущен
Write-Host "🛑 Stopping dev server..." -ForegroundColor Yellow
taskkill /F /IM node.exe 2>$null

# Очищаем все кэши и build файлы
Write-Host "🗑️ Cleaning cache directories..." -ForegroundColor Yellow
$directories = @(".nuxt", ".output", "dist", "node_modules\.cache")
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Remove-Item -Recurse -Force $dir
        Write-Host "✅ Removed $dir" -ForegroundColor Green
    }
}

# Очищаем npm кэш
Write-Host "🧹 Cleaning npm cache..." -ForegroundColor Yellow
npm cache clean --force

# Переустанавливаем зависимости
Write-Host "📦 Reinstalling dependencies..." -ForegroundColor Yellow
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
npm install

# Очищаем браузерный кэш (инструкции)
Write-Host "`n🌐 Browser Cache Instructions:" -ForegroundColor Yellow
Write-Host "1. Open browser DevTools (press F12)" -ForegroundColor White
Write-Host "2. Right-click on refresh button" -ForegroundColor White
Write-Host "3. Select 'Empty Cache and Hard Reload'" -ForegroundColor White
Write-Host "4. Or press Ctrl+Shift+R" -ForegroundColor White

# Запускаем dev сервер
Write-Host "`n🚀 Starting dev server..." -ForegroundColor Yellow
Write-Host "npm run dev" -ForegroundColor Cyan

Write-Host "`n✅ Clean and rebuild complete!" -ForegroundColor Green
Write-Host "📝 Don't forget to clear browser cache!" -ForegroundColor Yellow 