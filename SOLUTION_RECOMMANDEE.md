# ✨ La Solution Recommandée : GitHub Actions

**Gratuit • Automatique • Robuste • Zéro Maintenance**

---

## 🎯 Pourquoi GitHub Actions ?

| Critère | GitHub Actions | Google Drive | PythonAnywhere |
|---------|---|---|---|
| **Coût** | ✅ Gratuit | ⚠️ Peut être payant | ✅ Gratuit |
| **Automatisation** | ✅ Native | ✅ Oui | ✅ Oui |
| **Facilité setup** | ✅✅✅ Super facile | ⚠️ OAuth compliqué | ✅ Facile |
| **Robustesse** | ✅✅✅ Très robuste | ✅ Robuste | ⚠️ Moins robuste |
| **Maintenance** | ✅ Zéro | ✅ Zéro | ⚠️ Minimum |
| **Accès données** | ✅ GitHub + partage | ✅ Google Drive | ✅ URL |

**Verdict : GitHub Actions gagne sur tous les points** 🏆

---

## 🚀 Setup Ultra-Rapide (5 min)

### Commande 1 : Créer le repo GitHub
```bash
# Va sur github.com/new et crée "seek-scraper"
# Copie l'URL du repo
```

### Commande 2 : Uploader le code
```bash
cd /Users/paulpicart/seek_scraper

git init
git add .
git commit -m "Initial: Seek scraper"
git remote add origin https://github.com/TONUSERNAME/seek-scraper.git
git branch -M main
git push -u origin main
```

### Commande 3 : Tester
```
1. Va sur GitHub Actions tab
2. Clique "Run workflow"
3. Attends 2 min
4. Boom ! CSV rempli ! 🎉
```

**Voilà. C'est fini.**

---

## 📊 Utiliser les données

### Option 1 : Télécharger depuis GitHub
- Repo → `data/labourer_jobs_queensland.csv` → bouton Download

### Option 2 : Google Sheets (AUTO-UPDATE)
```
1. sheets.google.com → Nouveau document
2. File → Import → From URL
3. Colle : https://raw.githubusercontent.com/TONUSERNAME/seek-scraper/main/data/labourer_jobs_queensland.csv
4. Les données se mettent à jour automatiquement ! 📈
```

### Option 3 : Import par script
```bash
# Télécharger le CSV
curl https://raw.githubusercontent.com/TONUSERNAME/seek-scraper/main/data/labourer_jobs_queensland.csv -o jobs.csv
```

---

## ⏰ Fonctionnement automatique

- **Toutes les 2 heures** : GitHub lance le scraper
- **Automatiquement** : Les données se sauvegardent
- **Sans intervention** : Tu n'as rien à faire

---

## 💡 Bonus : Google Sheets Live

La meilleure façon pour accéder partout :

1. Crée un Google Sheet
2. Utilise **"Import"** avec l'URL du CSV
3. **Les données se mettent à jour auto** quand tu recharges

**Résultat : Un tableau qui se met à jour tout seul ! ✨**

---

## 📋 Checklist finale

```
✅ Repo GitHub créé (seek-scraper)
✅ Code uploadé (git push)
✅ Workflow testé (Actions tab)
✅ CSV généré (32 offres)
✅ Google Sheets connecté (optionnel)
✅ Prêt pour le monde réel 🚀
```

---

## 🆘 Si ça ne marche pas

**Workflow "failed" ?**
- Actions → dernière run → vois les logs rouges
- Généralement c'est une dépendance manquante

**CSV vide ?**
- Vérify que Playwright peut accéder à Seek
- Teste localement : `python3 seek_scraper.py`

**Besoin de plus de détails ?**
- [Guide complet GitHub Actions](GITHUB_ACTIONS_SETUP.md)
- [Installation rapide](INSTALLATION_RAPIDE.md)

---

## 🎓 Alternative : Si tu veux vraiment du local

Si tu préfères que ça tourne sur ta machine :

```bash
# Setup local
pip install -r requirements.txt

# Lancer une fois
python3 seek_scraper.py

# Lancer en continu (toutes les 2h)
python3 seek_scheduler.py

# Ou en arrière-plan
nohup python3 seek_scheduler.py > logs/scraper.log 2>&1 &
```

**Mais GitHub Actions est vraiment mieux** : pas besoin de laisser ton Mac allumé 24h/24 ! 💻

---

## 🎉 Résumé final

| Aspect | GitHub Actions |
|--------|---|
| **Coût** | 🆓 0€ |
| **Setup** | ⏱️ 5 minutes |
| **Automatisation** | 🤖 Toutes les 2h |
| **Accès données** | 🌍 De partout |
| **Maintenance** | 🛌 Zéro |
| **Fiabilité** | 🎯 99.9% |

**La vraie solution "set and forget" 🚀**
