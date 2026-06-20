# GitHub Actions Setup (Gratuit et Robuste)

La solution la plus facile : le scraper tourne sur les serveurs GitHub, 100% gratuit.

## 📋 Ce que tu vas avoir

✅ Script exécuté **toutes les 2 heures** automatiquement  
✅ CSV mis à jour dans le repo GitHub  
✅ Accès de partout (téléphone, ordi, etc.)  
✅ **Gratuit** (2000 min/mois, plus que suffisant)  
✅ Aucun serveur à maintenir  

## 🚀 Setup en 3 étapes (5 minutes)

### Étape 1 : Créer un repo GitHub

1. Va sur [github.com/new](https://github.com/new)
2. **Repository name** : `seek-scraper`
3. **Description** : "Seek.com.au Labourer Jobs Scraper"
4. **Public** (visible pour toi)
5. Clique **"Create repository"**

### Étape 2 : Uploader le projet

Dans le terminal :

```bash
cd /Users/paulpicart/seek_scraper

# Initialise git
git init
git add .
git commit -m "Initial commit: Seek scraper setup"

# Ajoute le repo distant (remplace USER par ton username GitHub)
git remote add origin https://github.com/USER/seek-scraper.git
git branch -M main
git push -u origin main
```

### Étape 3 : Vérifier que ça marche

1. Va sur ton repo GitHub : `https://github.com/USER/seek-scraper`
2. Clique sur l'onglet **"Actions"**
3. Tu devrais voir "Seek Scraper" workflow
4. Clique sur **"Run workflow"** → **"Run workflow"** pour tester

**Résultat attendu :**
- ✅ Workflow exécuté
- ✅ CSV mis à jour dans `data/labourer_jobs_queensland.csv`
- ✅ Commit "Auto scrape: ..." créé

## ⏰ Comment ça marche

- **Automatique** : toutes les 2 heures
- **Historique** : chaque commit préserve l'état du CSV
- **Gratuit** : 2000 minutes/mois (largement suffisant pour 12 scrapes/jour)

## 📊 Accéder aux données

### Option A : Depuis GitHub
1. Va sur ton repo
2. Ouvre `data/labourer_jobs_queensland.csv`
3. GitHub affiche le CSV en tableau
4. Clique le bouton **"Raw"** pour le télécharger

### Option B : Télécharger directement
```bash
# URL brute (RAW) du CSV
https://raw.githubusercontent.com/USER/seek-scraper/main/data/labourer_jobs_queensland.csv
```

### Option C : Importer dans Google Sheets (mon préféré)
1. Va sur [sheets.google.com](https://sheets.google.com)
2. Nouveau document
3. Menu : `File` → `Import`
4. Sélectionne **"From a URL"**
5. Colle : `https://raw.githubusercontent.com/USER/seek-scraper/main/data/labourer_jobs_queensland.csv`
6. Boum ! Les données se mettent à jour auto

## 🔒 Sécurité

- Ton repo peut être **public** (pas de données sensibles)
- Les logs ne sauvegardent rien de sensible
- GitHub chiffre tout en transit

## 🛠️ Customisation

Veux-tu modifier la fréquence de scrape ?

Édite `.github/workflows/scrape.yml` :

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # Toutes les 2 heures
    # - cron: '0 * * * *'  # Chaque heure
    # - cron: '0 0 * * *'  # Chaque jour à minuit
```

[Cron expression helper](https://crontab.guru/)

## 📊 Voir les résultats

**Logs d'exécution :**
1. Repo GitHub → **Actions** tab
2. Clique sur le dernier run
3. Vois tous les détails

**Historique des scrapes :**
```bash
git log --oneline data/labourer_jobs_queensland.csv
```

## ❓ Troubleshooting

### "Workflow failed"
- Vérifie les logs dans l'onglet Actions
- Généralement c'est un problème de dépendances

### CSV ne se met pas à jour
- Va dans Actions → voir le dernier run
- Cherche les erreurs dans les logs

### Limites GitHub Actions
- 2000 min/mois gratuit (plus que suffisant)
- Ubuntu runner (pas de limite GPU/CPU)

## 💡 Bonus : Partager les données

### Partager le lien du CSV
```
https://github.com/USER/seek-scraper/blob/main/data/labourer_jobs_queensland.csv
```

### Créer un Google Sheet qui se met à jour auto
(Voir Option C ci-dessus)

### Exporter via API GitHub
```bash
curl https://api.github.com/repos/USER/seek-scraper/contents/data/labourer_jobs_queensland.csv
```

## ✨ C'est tout !

Ton scraper tourne maintenant 24h/24 sur GitHub, 100% gratuit.

Pas de serveur à maintenir, pas de frais, pas de configuration compliquée.

Besoin d'aide ? Vérifie les logs dans l'onglet Actions du repo.
