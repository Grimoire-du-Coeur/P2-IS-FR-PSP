@echo off
chcp 65001 > nul
echo =========================================
echo       P2IS Image Lab - Demarrage
echo =========================================
echo.

:: Tuer les anciens processus pour eviter les conflits de port
echo Nettoyage des anciens processus...
taskkill /IM python.exe /F 2>nul

echo Verification des dependances Python...
python -m pip install -r "%~dp0..\..\requirements.txt" --quiet

echo.
echo Lancement du serveur...
cd /d "%~dp0..\.."
python -m labs.image.server.server_image
