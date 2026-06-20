#!/bin/bash
# Script pour configurer rapidement Google Drive

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "☁️  Configuration Google Drive Sync"
echo "===================================="
echo ""

# Vérifie si le fichier de credentials existe
if [ -f "google_credentials.json" ]; then
    echo "✅ google_credentials.json trouvé"
else
    echo "❌ google_credentials.json non trouvé"
    echo ""
    echo "Étapes pour obtenir les identifiants :"
    echo "1. Visite: https://console.cloud.google.com/"
    echo "2. Crée un nouveau projet: 'Seek-Scraper'"
    echo "3. Active l'API Google Drive"
    echo "4. Crée des identifiants OAuth (Desktop app)"
    echo "5. Télécharge le JSON et renomme-le en 'google_credentials.json'"
    echo "6. Place-le dans ce dossier: $SCRIPT_DIR"
    echo ""
    echo "Voir GOOGLE_DRIVE_SETUP.md pour les détails complets"
    exit 1
fi

echo ""
echo "🔄 Test de synchronisation..."
echo ""

# Lance le scraper avec Google Drive sync
python3 seek_scraper.py

echo ""
echo "✅ Configuration terminée !"
echo ""
echo "📊 Résultats :"
echo "   - CSV local : data/labourer_jobs_queensland.csv"
echo "   - Google Drive : Seek-Scraper-Data/labourer_jobs_queensland.csv"
echo ""
echo "💡 Prochaines fois :"
echo "   Le scraper synchronisera automatiquement sans interaction"
echo ""
