# 🚀 Installation Rapide - GitHub Actions

**La solution la plus facile et gratuite : 3 étapes, 5 minutes**

---

## ✅ Étape 1 : Créer un repo GitHub

1. Va sur [github.com/new](https://github.com/new)
2. **Repository name** : `seek-scraper`
3. Clique **"Create repository"**
4. **Copie l'URL** du repo (ex: `https://github.com/tonusername/seek-scraper.git`)

---

## ✅ Étape 2 : Uploader le projet

Ouvre un terminal et exécute :

```bash
cd /Users/paulpicart/seek_scraper

git init
git add .
git commit -m "Initial commit: Seek scraper"

# Remplace TONUSERNAME par ton username GitHub
git remote add origin https://github.com/TONUSERNAME/seek-scraper.git
git branch -M main
git push -u origin main
```

**C'est tout !** Le code est maintenant sur GitHub.

---

## ✅ Étape 3 : Tester le workflow

1. Va sur ton repo GitHub
2. Clique sur l'onglet **"Actions"**
3. Clique sur **"Seek Scraper"** workflow
4. Clique **"Run workflow"** → **"Run workflow"**

**Attends 2-3 minutes...**

✅ Le workflow s'exécute  
✅ Le CSV se remplit avec les 32 offres  
✅ Un commit est créé automatiquement  

---

## 🎉 C'est fini !

Ton scraper tourne maintenant **toutes les 2 heures** sans rien faire d'autre.

### 📊 Accéder au CSV

**Option A : GitHub (simple)**
- Repo → `data/labourer_jobs_queensland.csv`
- Clique **"Raw"** pour télécharger

**Option B : Google Sheets (auto-update)**
1. Nouveau Google Sheet
2. `File` → `Import`
3. URL : `https://raw.githubusercontent.com/TONUSERNAME/seek-scraper/main/data/labourer_jobs_queensland.csv`
4. Les données se mettent à jour auto ! 📈

---

## 📋 Checklist

- [ ] Repo GitHub créé
- [ ] Code uploadé avec `git push`
- [ ] Workflow testé (Actions tab)
- [ ] CSV généré et visible
- [ ] Prêt pour l'automation 24h/24

---

## ❓ Besoin d'aide ?

**Workflow ne s'exécute pas ?**
- Vérifie les logs : Actions → dernier run → voir les erreurs

**CSV ne se met à jour ?**
- Regarde les logs du dernier run
- Vérifie que Playwright est installé

**Modifier la fréquence ?**
- Édite `.github/workflows/scrape.yml`
- Change le `cron` schedule

---

## 🎓 Ressources

- [Guide complet GitHub Actions Setup](GITHUB_ACTIONS_SETUP.md)
- [Cron scheduler helper](https://crontab.guru/)
- [GitHub Actions docs](https://docs.github.com/en/actions)

---

**Résumé :**
- ✅ Gratuit (2000 min/mois)
- ✅ Automatique (toutes les 2h)
- ✅ Robuste (GitHub gère tout)
- ✅ Accessible partout
- ✅ Aucun serveur à maintenir

C'est la solution "set and forget" parfaite ! 🚀
