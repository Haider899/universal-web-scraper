@echo off
echo ========================================
echo    UNIVERSAL WEB SCRAPER PRO - WINDOWS
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

:: Install packages
echo 📦 Installing dependencies...
pip install requests beautifulsoup4 pandas openpyxl lxml

echo.
echo ✅ Installation complete!
echo 🚀 Starting Universal Web Scraper...
echo.

:: Run the scraper
python advanced_scraper.py

:: Keep window open
pause
