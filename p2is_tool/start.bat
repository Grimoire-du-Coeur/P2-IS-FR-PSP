@echo off
chcp 65001 > nul
echo ==============================================================
echo       P2IS FR Translation Tool - Demarrage
echo ==============================================================
echo.

:: Tuer les anciens processus pour eviter les conflits de port
echo Nettoyage des anciens processus...
FOR /F "tokens=5" %%a IN ('netstat -aon ^| find ":8000" ^| find "LISTENING"') DO taskkill /F /PID %%a 2>nul
taskkill /IM python.exe /F 2>nul
taskkill /IM python3.* /F 2>nul

echo Verification des dependances Python...
python -m pip install -r requirements.txt --quiet

echo.
echo Lancement du serveur...
cd /d "%~dp0server"
python server.py

echo.
echo Le serveur s'est arrete (ou a crash).
pause
