# Google Drive Synchronization Setup

Synchronise automatiquement les offres d'emploi vers Google Drive pour y accéder de partout.

## 🔐 Étape 1 : Créer des identifiants Google Cloud

### 1.1 Ouvrir Google Cloud Console
Visite [Google Cloud Console](https://console.cloud.google.com/)

### 1.2 Créer un nouveau projet
1. Clique sur **"Select a Project"** en haut
2. Clique sur **"NEW PROJECT"**
3. Donne un nom : `Seek-Scraper`
4. Clique **"CREATE"**

### 1.3 Activer Google Drive API
1. Dans la barre de recherche, tape `Google Drive API`
2. Clique sur le résultat et clique **"ENABLE"**

### 1.4 Créer les identifiants OAuth 2.0
1. Va à **"Credentials"** dans le menu gauche
2. Clique **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Sélectionne **"Desktop application"** (si demandé: "User Data")
4. Clique **"CREATE"**
5. Clique sur l'icône de téléchargement (⬇️) pour télécharger le JSON

### 1.5 Renommer et placer le fichier
1. Renomme le fichier téléchargé en `google_credentials.json`
2. Place-le dans le dossier du projet :
   ```
   /Users/paulpicart/seek_scraper/google_credentials.json
   ```

## 🚀 Étape 2 : Installer les dépendances

```bash
cd /Users/paulpicart/seek_scraper
pip install -r requirements.txt
```

## ✅ Étape 3 : Premier lancement avec authentification

```bash
cd /Users/paulpicart/seek_scraper
python3 seek_scraper.py
```

**Première fois seulement :**
- Un navigateur s'ouvrira pour l'authentification Google
- Clique **"Allow"** pour autoriser l'accès à Google Drive
- Le script continuera automatiquement
- Un token sera sauvegardé pour les prochaines fois

**Les fois suivantes :**
- Aucune interaction requise
- Le token sauvegardé sera utilisé automatiquement

## 📊 Résultat

Après le premier lancement :
- Un dossier **`Seek-Scraper-Data`** sera créé sur ton Google Drive
- Le fichier **`labourer_jobs_queensland.csv`** sera uploadé
- Chaque nouveau scrape mettra à jour le fichier sur Google Drive

**Accès depuis n'importe où :**
```
https://drive.google.com/drive/folders/[folder-id]
```

## ⚙️ Configuration

Pour modifier les paramètres, édite `config.py` :

```python
ENABLE_GOOGLE_DRIVE = True                    # Active/désactive
GOOGLE_DRIVE_FOLDER_NAME = "Seek-Scraper-Data"   # Nom du dossier
```

## 🔧 Troubleshooting

### "Credentials file not found"
Assure-toi que `google_credentials.json` est dans `/Users/paulpicart/seek_scraper/`

### "Permission denied"
1. Va à Google Cloud Console
2. Vérifie que l'API Google Drive est activée
3. Les identifiants incluent les permissions Google Drive

### Réinitialiser l'authentification
Supprime le token sauvegardé et relance :
```bash
rm /Users/paulpicart/seek_scraper/google_token.pickle
python3 seek_scraper.py
```

### Vérifier les logs
```bash
tail -f /Users/paulpicart/seek_scraper/logs/scraper.log
```

## 🔒 Sécurité

- Les credentials sont sauvegardés localement (ne jamais les partager)
- Le token est réutilisé et rafraîchi automatiquement
- Aucun mot de passe stocké en clair
- Les permissions sont limitées à Google Drive uniquement

## 💡 Astuces

### Partager le dossier Google Drive
1. Va sur Google Drive
2. Clique droit sur `Seek-Scraper-Data`
3. **"Share"** → Ajoute les adresses email
4. Les collaborateurs ont accès aux CSV

### Créer un lien public (lecture seule)
1. Partage le dossier avec "Anyone with the link"
2. Copie le lien
3. Partage avec qui tu veux (sans édition)

### Télécharger le CSV depuis Google Drive
- Simple clic droit → **Download**
- Ou utilise Google Sheets pour analyser directement

## 📝 Logs

Les logs incluent les détails de chaque sync :
```
2026-06-20 15:30:45 - INFO - ✓ Found Google Drive folder
2026-06-20 15:30:50 - INFO - ✓ Updated file on Google Drive: labourer_jobs_queensland.csv
```

## ❓ Questions

Si tu rencontres des problèmes :
1. Vérifie les logs : `tail -f logs/scraper.log`
2. Assure-toi que tu as une connexion Internet
3. Vérifie que ton compte Google est actif
4. Essaie de réinitialiser le token (voir Troubleshooting)
