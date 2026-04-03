# Fristine Presales Portal - Windows Startup Script
# Usage: .\scripts\start-app.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Fristine Presales Portal - Start App" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Detect Root and Venv
$RepoRoot = Get-Item "."
$VenvPath = Join-Path $RepoRoot.Parent.FullName ".venv"

if (-not (Test-Path "$VenvPath\Scripts\python.exe")) {
    Write-Host "Error: Virtual environment not found at $VenvPath" -ForegroundColor Red
    Write-Host "Please ensure .venv is in $( $RepoRoot.Parent.FullName )" -ForegroundColor Yellow
    exit
}

# 2. Start Backend
Write-Host "`n[1/3] Starting Backend (Port 8000)..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd backend; & '$VenvPath\Scripts\activate.ps1'; python main.py"

# 3. Start Frontend
Write-Host "[2/3] Starting Frontend (Port 5173)..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

# 4. Start Localtunnel (Optional but recommended for Voice)
$Subdomain = "fristine-ai-bot"
Write-Host "[3/3] Starting Localtunnel ($Subdomain.loca.lt)..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "lt --port 8000 --subdomain $Subdomain"

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "  All services initiated in new windows." -ForegroundColor Cyan
Write-Host "  - Backend: http://localhost:8000"
Write-Host "  - Frontend: http://localhost:5173"
Write-Host "  - Public Tunnel: https://$Subdomain.loca.lt"
Write-Host "==========================================" -ForegroundColor Cyan
