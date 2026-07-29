@echo off
echo =========================================
echo       P2IS Audio Lab - Demarrage
echo =========================================
echo.

:: 1. Demarrer le serveur backend Python en arriere-plan
echo Lancement du serveur Python (Backend)...
start /min cmd /c "cd server && uvicorn server_audio:app --host 127.0.0.1 --port 8001"

:: Attendre que le backend s'initialise (remplace timeout)
ping 127.0.0.1 -n 3 > nul

:: 2. Installer les dependances Node si necessaire et lancer le frontend
echo.
echo Verification de l'interface web (Frontend)...
cd web_ui

if not exist "node_modules\" (
    echo.
    echo ---------------------------------------------------
    echo Installation des dependances pour la premiere fois...
    echo Cela peut prendre quelques instants...
    echo ---------------------------------------------------
    call npm install
)

echo.
echo Lancement de l'interface web...
call npm run dev -- --open
