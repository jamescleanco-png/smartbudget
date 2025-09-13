@echo off
echo 🚀 Démarrage de l'application de gestion financière...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo 📦 Vérification des dépendances...
pip install -r requirements.txt

REM Démarrer l'application
echo.
echo 🌐 Démarrage du serveur...
echo 📍 L'application sera accessible à l'adresse: http://localhost:5000
echo ⏹️  Appuyez sur Ctrl+C pour arrêter le serveur
echo.

python app.py
pause
