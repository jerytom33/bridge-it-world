# Quick Setup Script for MegaLLM Integration
# Run this script to set environment variables and test the integration

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "MegaLLM Backend Integration Setup" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Set environment variables
Write-Host "[1/3] Setting environment variables..." -ForegroundColor Yellow
$env:MEGALLM_API_KEY = "sk-mega-51c1ea28e101197977ad76e5d4446be7fdc5d0e2f45a92060e4d82a8d4c51839"
$env:MEGALLM_BASE_URL = "https://ai.megallm.io/v1"
$env:MEGALLM_MODEL = "gpt-4o-mini"
Write-Host "✅ Environment variables set!" -ForegroundColor Green
Write-Host ""

# Test the integration
Write-Host "[2/3] Testing MegaLLM service..." -ForegroundColor Yellow
python test_megallm.py
Write-Host ""

# Show next steps
Write-Host "[3/3] Next Steps:" -ForegroundColor Yellow
Write-Host "  1. To start the Django server with MegaLLM enabled:" -ForegroundColor White
Write-Host "     python manage.py runserver 0.0.0.0:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Test the new endpoints from your Flutter app:" -ForegroundColor White
Write-Host "     GET  /api/aptitude/personalized-questions/?level=12th" -ForegroundColor Gray
Write-Host "     POST /api/aptitude/analyze-results/" -ForegroundColor Gray
Write-Host "     POST /api/resume/upload/ (now includes MegaLLM analysis)" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. For detailed documentation, see:" -ForegroundColor White
Write-Host "     MEGALLM_INTEGRATION_GUIDE.md" -ForegroundColor Gray
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
