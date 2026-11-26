@echo off
chcp 65001 > nul
echo =========================================
echo       P2IS Audio Lab - Demarrage
echo =========================================
echo.

:: Tuer les anciens processus occupant le port 8001
echo Nettoyage des anciens processus...
FOR /F "tokens=5" %%a IN ('netstat -aon ^| find ":8001" ^| find "LISTENING"') DO taskkill /F /PID %%a 2>nul

echo Verification des dependances Python...
python -m pip install -r "%~dp0..\..\requirements.txt" --quiet

echo.
echo Lancement du serveur...
cd /d "%~dp0..\.."
python -m labs.audio.server.server_audio

echo.
echo Le serveur s'est arrete (ou a crash).
pause
