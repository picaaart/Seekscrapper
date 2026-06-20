"""Configuration pour le scraper Seek.com.au"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# URLs et recherche
SEEK_URL = "https://www.seek.com.au/labourer-jobs/in-Queensland"
JOB_TITLE = "labourer"
LOCATION = "Queensland"

# Fichiers
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
OUTPUT_CSV = os.path.join(DATA_DIR, 'labourer_jobs_queensland.csv')
LOG_FILE = os.path.join(LOGS_DIR, 'scraper.log')

# Timing
SCRAPE_INTERVAL_HOURS = 2  # Scrape toutes les 2 heures
TIMEOUT_SECONDS = 60

# Browser
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
HEADLESS = True

# Google Drive (optionnel)
ENABLE_GOOGLE_DRIVE = False  # Active/désactive la sync Google Drive
GOOGLE_DRIVE_FOLDER_NAME = "Seek-Scraper-Data"
GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'google_credentials.json')
GOOGLE_TOKEN_FILE = os.path.join(BASE_DIR, 'google_token.pickle')

# Créer les dossiers s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
