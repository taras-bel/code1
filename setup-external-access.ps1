# Setup External Access for NoaMetrics
# This script helps configure the application for external access

Write-Host "🔧 Setting up external access for NoaMetrics..." -ForegroundColor Cyan

# Get external IP
Write-Host "📡 Getting external IP address..." -ForegroundColor Yellow
try {
    $externalIP = (Invoke-WebRequest -Uri "https://ifconfig.me" -UseBasicParsing).Content.Trim()
    Write-Host "✅ External IP: $externalIP" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to get external IP. Please enter it manually:" -ForegroundColor Red
    $externalIP = Read-Host "External IP"
}

# Get local IP
Write-Host "🏠 Getting local IP address..." -ForegroundColor Yellow
try {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
    Write-Host "✅ Local IP: $localIP" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to get local IP. Please enter it manually:" -ForegroundColor Red
    $localIP = Read-Host "Local IP"
}

# Create or update .env file
Write-Host "📝 Updating environment configuration..." -ForegroundColor Yellow

$envContent = @"
# External Access Configuration
EXTERNAL_IPS=$externalIP,$localIP

# Add your external IP to CORS origins
# The application will automatically allow access from these IPs
"@

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "📄 Updating existing .env file..." -ForegroundColor Yellow
    
    # Read existing content
    $existingContent = Get-Content ".env" -Raw
    
    # Check if EXTERNAL_IPS already exists
    if ($existingContent -match "EXTERNAL_IPS=") {
        # Update existing EXTERNAL_IPS
        $updatedContent = $existingContent -replace "EXTERNAL_IPS=.*", "EXTERNAL_IPS=$externalIP,$localIP"
        Set-Content ".env" $updatedContent
    } else {
        # Add EXTERNAL_IPS to existing file
        Add-Content ".env" "`n# External Access Configuration`nEXTERNAL_IPS=$externalIP,$localIP"
    }
} else {
    Write-Host "📄 Creating new .env file..." -ForegroundColor Yellow
    Set-Content ".env" $envContent
}

Write-Host "✅ Environment configuration updated!" -ForegroundColor Green

# Display access information
Write-Host "`n🌐 Access Information:" -ForegroundColor Cyan
Write-Host "   Local Access:     https://localhost" -ForegroundColor White
Write-Host "   Network Access:   https://$localIP" -ForegroundColor White
Write-Host "   External Access:  https://$externalIP" -ForegroundColor White

Write-Host "`n🔧 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Restart the application: ./stop-https.ps1 && ./start-https.ps1" -ForegroundColor White
Write-Host "   2. Configure port forwarding on your router:" -ForegroundColor White
Write-Host "      - Port 80 (HTTP) -> $localIP:80" -ForegroundColor White
Write-Host "      - Port 443 (HTTPS) -> $localIP:443" -ForegroundColor White
Write-Host "   3. Test external access: https://$externalIP" -ForegroundColor White

Write-Host "`n✅ External access setup complete!" -ForegroundColor Green 