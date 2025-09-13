#!/bin/bash

echo "🚀 Démarrage de l'application de gestion financière..."
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip install -r requirements.txt

# Démarrer l'application
echo ""
echo "🌐 Démarrage du serveur..."
echo "📍 L'application sera accessible à l'adresse: http://localhost:5000"
echo "⏹️  Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python app.py
