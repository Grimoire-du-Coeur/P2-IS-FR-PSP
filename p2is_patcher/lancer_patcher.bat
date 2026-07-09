@echo off
echo ========================================
echo  Patcher Web - Persona 2 IS FR
echo  Lancement du serveur local...
echo ========================================
echo.
echo Le navigateur va s'ouvrir automatiquement sur :
echo http://localhost:8080
echo.
echo Appuyez sur Ctrl+C dans cette fenetre pour arreter.
echo.

cd /d "%~dp0"
start http://localhost:8080

python -m http.server 8080 2>nul || (
    echo Python non trouve, essai avec npx...
    npx serve . -p 8080
)
