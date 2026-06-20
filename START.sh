#!/bin/bash
# Script de démarrage rapide pour le scraper Seek

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🔍 Seek.com.au Labourer Job Scraper"
echo "=================================="
echo ""
echo "Options de démarrage :"
echo "1) Test rapide (une seule fois)"
echo "2) Scheduler continu (toutes les 2 heures, dans le terminal)"
echo "3) Arrière-plan (nohup, peut fermer le terminal)"
echo ""
read -p "Choisis une option (1-3) : " choice

case $choice in
    1)
        echo ""
        echo "🚀 Lancement d'un test unique..."
        python3 seek_scraper.py
        echo ""
        echo "✅ Fini ! Regarde data/labourer_jobs_queensland.csv"
        ;;
    2)
        echo ""
        echo "🔄 Lancement du scheduler (Ctrl+C pour arrêter)..."
        python3 seek_scheduler.py
        ;;
    3)
        echo ""
        echo "🌙 Lancement en arrière-plan..."
        nohup python3 seek_scheduler.py > nohup.log 2>&1 &
        PID=$!
        echo "✅ Scraper démarré (PID: $PID)"
        echo "   Logs: nohup.log"
        echo "   Arrête avec: kill $PID"
        ;;
    *)
        echo "❌ Option invalide"
        exit 1
        ;;
esac
