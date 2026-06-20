# Seek.com.au Labourer Job Scraper

Scrape labourer job listings from Seek.com.au (Queensland) and automatically save them to CSV format.

## 📁 Structure du projet

```
seek_scraper/
├── seek_scraper.py          # Script principal de scraping
├── seek_scheduler.py        # Scheduler pour exécution automatique
├── config.py               # Configuration centralisée
├── requirements.txt        # Dépendances Python
├── README.md              # Ce fichier
├── data/                  # Dossier des fichiers CSV générés
│   └── labourer_jobs_queensland.csv
├── logs/                  # Dossier des fichiers log
│   └── scraper.log
└── utils/                 # Utilitaires additionnels
```

## 🚀 Installation rapide

### 1. Installer les dépendances
```bash
cd /Users/paulpicart/seek_scraper
pip install -r requirements.txt
python3 -m playwright install chromium
```

### 2. Premier test
```bash
python3 seek_scraper.py
```

Cela devrait créer `data/labourer_jobs_queensland.csv` avec les offres d'emploi.

## ☁️ Google Drive Synchronization

Le scraper synchronise automatiquement le CSV vers Google Drive !

**Configuration rapide :**
```bash
# Voir le guide complet
cat GOOGLE_DRIVE_SETUP.md
```

**Avantages :**
- ✅ Accède au CSV de n'importe où
- ✅ Auto-sync après chaque scrape
- ✅ Partage facile avec d'autres
- ✅ Backup automatique

**Après le setup :**
- Un dossier `Seek-Scraper-Data` apparaît sur ton Google Drive
- Le CSV est mis à jour automatiquement toutes les 2 heures

[Guide complet de configuration →](GOOGLE_DRIVE_SETUP.md)

## 🔄 Utilisation

### Option A : Lancer une seule fois
```bash
cd /Users/paulpicart/seek_scraper
python3 seek_scraper.py
```

### Option B : Scheduler continu (scrape toutes les 2 heures)

**Terminal foreground :**
```bash
cd /Users/paulpicart/seek_scraper
python3 seek_scheduler.py
```
Le terminal doit rester ouvert. Press Ctrl+C pour arrêter.

**Arrière-plan avec nohup :**
```bash
cd /Users/paulpicart/seek_scraper
nohup python3 seek_scheduler.py > nohup.log 2>&1 &
```

Vérifie le processus :
```bash
ps aux | grep seek_scheduler
```

Tue le processus :
```bash
pkill -f seek_scheduler
```

### Option C : Daemon macOS (launchd) - À l'arrière-plan au démarrage

1. Crée le fichier plist :
```bash
cat > ~/Library/LaunchAgents/com.seek.scraper.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.seek.scraper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/paulpicart/seek_scraper/seek_scheduler.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>7200</integer>
    <key>StandardOutPath</key>
    <string>/Users/paulpicart/seek_scraper/logs/scheduler.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/paulpicart/seek_scraper/logs/scheduler_error.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/paulpicart/seek_scraper</string>
</dict>
</plist>
EOF
```

2. Charge le service :
```bash
launchctl load ~/Library/LaunchAgents/com.seek.scraper.plist
```

3. Vérifie l'état :
```bash
launchctl list | grep seek.scraper
```

4. Arrête le service :
```bash
launchctl unload ~/Library/LaunchAgents/com.seek.scraper.plist
```

## 📊 Données générées

**Fichier CSV :** `data/labourer_jobs_queensland.csv`

Colonnes :
- **title** : Titre du poste (ex: "Construction Labourer")
- **company** : Nom de l'entreprise
- **location** : Localisation (ex: "Brisbane QLD")
- **job_type** : Type d'emploi (Full-time, Part-time, Contract, Casual)
- **salary** : Salaire/taux horaire quand disponible
- **url** : Lien direct vers l'annonce Seek
- **scraped_at** : Timestamp du scrape

## ⚙️ Configuration

Modifie `config.py` pour personnaliser :

```python
SCRAPE_INTERVAL_HOURS = 2        # Intervalle de scraping
SEEK_URL = "..."                 # URL à scraper
HEADLESS = True                  # Mode headless du navigateur
TIMEOUT_SECONDS = 60             # Timeout de chargement
```

## 📋 Logs

Les logs sont sauvegardés dans `logs/scraper.log` avec :
- Timestamps
- Niveau de sévérité (INFO, WARNING, ERROR)
- Messages détaillés

Affiche les logs :
```bash
tail -f /Users/paulpicart/seek_scraper/logs/scraper.log
```

## 🔧 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
python3 -m playwright install chromium
```

### CSV pas de mise à jour
Vérifie les logs :
```bash
cat /Users/paulpicart/seek_scraper/logs/scraper.log
```

### Seek bloque les requêtes
- Augmente `TIMEOUT_SECONDS` dans config.py
- Vérifie les logs pour les erreurs Cloudflare
- Essaie manuellement depuis un navigateur pour vérifier que le site est accessible

## 📝 Notes

- Respecte les pratiques de scraping : intervalle de 2h entre les requêtes
- Pas d'authentification requise pour les listings publics Seek
- Les données s'ajoutent au CSV sans duplication de headers
- Tous les logs sont tracés pour faciliter le debugging

## 🆘 Support

Pour des questions ou des problèmes, vérifie :
1. `logs/scraper.log` pour les erreurs
2. La connexion Internet
3. Que Seek.com.au est accessible depuis un navigateur normal
4. Les permissions du dossier `data/` pour la lecture/écriture
