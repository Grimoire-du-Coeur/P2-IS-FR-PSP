@echo off
echo ==============================================================
echo       P2IS FR Translation Tool - Server Startup
echo ==============================================================
echo.

echo [1/4] Installation des dependances Python...
python -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo Erreur lors de l'installation des dependances Python.
    pause
    exit /b
)

echo [2/4] Demarrage du backend (FastAPI)...
start "P2IS Backend" cmd /c "python server.py"

echo [3/4] Verification des dependances frontend...
cd web_ui
if not exist node_modules (
    echo Installation de npm... (peut prendre une minute la premiere fois)
    call npm install
)

echo [4/4] Demarrage du frontend (Vite)...
start "P2IS Frontend" cmd /c "npm run dev"

echo.
echo L'application se lance dans votre navigateur par defaut...
timeout /t 3 /nobreak >nul
start http://localhost:5173
