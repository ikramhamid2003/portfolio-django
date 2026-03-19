# ============================================================
# setup.ps1  —  Ikram Hamid Portfolio · Windows PowerShell
# Run: .\setup.ps1
# ============================================================
Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║   Ikram Hamid Portfolio — Setup Script   ║" -ForegroundColor Yellow
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

# 1. Virtual environment
Write-Host "[1/8] Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}
.\venv\Scripts\Activate.ps1

# 2. Dependencies
Write-Host "[2/8] Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# 3. .env setup
Write-Host ""
Write-Host "[3/8] Database Configuration" -ForegroundColor Cyan
Write-Host "  Choose database:" -ForegroundColor White
Write-Host "  [1] Neon PostgreSQL (recommended for production)" -ForegroundColor White
Write-Host "  [2] SQLite (local dev only, no setup needed)" -ForegroundColor White
$dbChoice = Read-Host "  Enter choice (1 or 2)"

if ($dbChoice -eq "1") {
    Write-Host ""
    Write-Host "  Paste your Neon DATABASE_URL from https://console.neon.tech" -ForegroundColor Yellow
    Write-Host "  Format: postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require" -ForegroundColor Gray
    $dbUrl = Read-Host "  DATABASE_URL"
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | % {[char]$_})
    @"
SECRET_KEY=$secretKey
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=$dbUrl
"@ | Set-Content .env
    Write-Host "  .env created with Neon PostgreSQL" -ForegroundColor Green
} else {
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | % {[char]$_})
    @"
SECRET_KEY=$secretKey
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=
"@ | Set-Content .env
    Write-Host "  .env created — using SQLite fallback" -ForegroundColor Green
}

# 4. Migrations
Write-Host ""
Write-Host "[4/8] Running migrations..." -ForegroundColor Cyan
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Migration failed. Check your DATABASE_URL in .env" -ForegroundColor Red
    exit 1
}

# 5. Seed data
Write-Host "[5/8] Seeding portfolio data from resume..." -ForegroundColor Cyan
python manage.py seed_data

# 6. Superuser
Write-Host ""
Write-Host "[6/8] Create admin superuser for Analytics access? (y/n)" -ForegroundColor Cyan
$createAdmin = Read-Host
if ($createAdmin -eq 'y') {
    python manage.py createsuperuser
}

# 7. Static files
Write-Host "[7/8] Collecting static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput

# 8. Launch
Write-Host ""
Write-Host "[8/8] Starting server..." -ForegroundColor Green
Write-Host ""
Write-Host "  ┌─────────────────────────────────────────────┐" -ForegroundColor White
Write-Host "  │  Portfolio  →  http://127.0.0.1:8000        │" -ForegroundColor White
Write-Host "  │  Admin      →  http://127.0.0.1:8000/admin  │" -ForegroundColor White
Write-Host "  │  Analytics  →  http://127.0.0.1:8000/analytics/login  │" -ForegroundColor White
Write-Host "  └─────────────────────────────────────────────┘" -ForegroundColor White
Write-Host ""
python manage.py runserver
