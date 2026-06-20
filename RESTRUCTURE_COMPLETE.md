# 🚀 Restructuration Complète - FAIT !

**Version 2.0 : Multi-Category Scraper avec Nettoyage Automatique**

---

## ✅ Quoi de neuf ?

### 1️⃣ **10 Catégories de Jobs**

```
✅ Construction        (labourer, carpenter, electrician, etc.)
✅ FIFO / Mines        (truck driver, operator, drill, etc.)
✅ Agriculture/Farms   (fruit picker, farm hand, etc.)
✅ Logistics/Transport (truck driver, forklift, warehouse, etc.)
✅ Hospitality        (chef, waiter, barista, etc.)
✅ Healthcare         (aged care, support worker, etc.)
✅ Retail             (sales, cashier, stock, etc.)
✅ Warehouse          (packer, picker, loader, etc.)
✅ Security           (security guard, bouncer, etc.)
✅ Cleaning           (cleaner, housekeeper, janitor, etc.)
```

### 2️⃣ **8 États d'Australie**

```
✅ Queensland (QLD)
✅ New South Wales (NSW)
✅ Victoria (VIC)
✅ Western Australia (WA)
✅ South Australia (SA)
✅ Tasmania (TAS)
✅ Northern Territory (NT)
✅ Australian Capital Territory (ACT)
```

### 3️⃣ **Nettoyage Automatique des Données**

```
✅ Supprime les offres de plus de 30 jours
✅ Archive les vieilles données
✅ CSV toujours léger et à jour
✅ Historique complet préservé
```

---

## 📊 Fichiers Générés

```
data/
├── jobs_australia_current.csv    ← Offres actuelles (< 30 jours) 📈
└── jobs_australia_archive.csv    ← Tout l'historique 📚
```

**Structure du CSV :**
```
title | company | location | state | job_category | job_keyword | job_type | salary | url | scraped_at
```

**Exemple de données :**
```
Labourer | XYZ Co | Brisbane | QLD | Construction | labourer | Contract | $40/h | ... | 2026-06-20
Fruit Picker | Farm ABC | Shepparton | VIC | Agriculture | fruit picker | Casual | $25/h | ... | 2026-06-20
Truck Driver | Mining Co | Kalgoorlie | WA | FIFO/Mines | truck driver | Full-time | $80k/year | ... | 2026-06-20
Chef | Restaurant | Melbourne | VIC | Hospitality | chef | Full-time | $50k/year | ... | 2026-06-20
Forklift Operator | Warehouse Co | Sydney | NSW | Warehouse | forklift operator | Full-time | $45k/year | ... | 2026-06-20
```

---

## 🔧 Architecture Nouvelle

### `jobs_config.py` (Configuration Centralisée)
```python
JOBS_CATEGORIES = {
    "construction": {
        "display_name": "Construction",
        "keywords": ["labourer", "carpenter", "electrician", ...]
    },
    "fifo_mines": {...},
    "agriculture": {...},
    # ... 10 catégories totales
}

AUSTRALIAN_STATES = {"QLD": "Queensland", "NSW": ..., ...}

DATA_RETENTION_DAYS = 30  # Garder 1 mois
```

**Avantage :** Facile d'ajouter de nouvelles catégories, jobs, ou états !

### `data_cleaner.py` (Nettoyage Automatique)
```python
class DataCleaner:
    - Supprime les offres expirées
    - Archive les vieilles données
    - Log les actions
```

### `seek_scraper.py` (Scraper Multi-Catégorie)
```python
class MultiCategorySeekScraper:
    - Boucle sur toutes les catégories
    - Boucle sur tous les états
    - Boucle sur tous les job keywords
    - Scrape Seek pour chaque combinaison
    - Sauvegarde dans le CSV
    - Nettoie automatiquement
```

---

## 🔄 Workflow GitHub Actions Amélioré

**`.github/workflows/scrape.yml`**

```yaml
Toutes les 2 heures :
  1. Scrape TOUS les jobs (10 catégories × 8 états)
  2. Ajoute au CSV courant
  3. Archive les vieilles données (> 30 jours)
  4. Commit et push sur GitHub
  5. Logs sauvegardés
```

**Résultat :**
- ✅ **Centaines de jobs** scrappés toutes les 2h
- ✅ **CSV toujours à jour** et propre
- ✅ **Historique complet** préservé
- ✅ **Zéro maintenance** manuelle

---

## 📈 Statistiques Attendues

**Par scrape (toutes les 2h) :**
```
~ 10 catégories × 8 états × plusieurs jobs par requête
= Potentiellement 500-2000+ nouvelles offres par scrape
```

**Par jour :**
```
12 scrapes × 500-2000 offres = 6,000-24,000 offres/jour
```

**Par mois :**
```
~ 180,000-720,000 offres
(Mais garder seulement les 30 jours = base toujours gérable)
```

---

## 🎯 Comment Utiliser

### Option A : GitHub (Recommandé)
```
1. Va sur https://github.com/picaaart/Seekscrapper
2. Actions tab → Run workflow
3. Attends 30-60 min pour le premier scrape complet
4. CSV rempli avec des centaines de jobs ! 📊
```

### Option B : Google Sheets (Auto-Update)
```
1. sheets.google.com → Nouveau document
2. File → Import → From URL
3. Colle : https://raw.githubusercontent.com/picaaart/Seekscrapper/main/data/jobs_australia_current.csv
4. Les données se mettent à jour toutes les 2h ! 🔄
```

### Option C : Télécharger le CSV
```
GitHub → data/jobs_australia_current.csv → Download
```

---

## 🧹 Nettoyage Automatique

**Qu'est-ce qui se passe ?**

```
Jour 1 : Scrape 1000 offres → CSV : 1000 lignes
Jour 2 : Scrape 1000 nouvelles → CSV : 2000 lignes
...
Jour 31 : Scrape + Archive les offres du Jour 1 → CSV : 1000 lignes (seulement récentes)
       + Historique complet dans archive
```

**Résultat :**
- ✅ CSV courant = offres fraîches et pertinentes
- ✅ Archive = tout l'historique
- ✅ Données toujours optimisées

---

## 🚀 Prochaines Étapes (Optionnel)

### Possibilité 1 : Ajouter plus de catégories
```python
# Dans jobs_config.py, ajoute simplement une nouvelle catégorie
"real_estate": {
    "display_name": "Real Estate",
    "keywords": ["real estate agent", "property manager", ...]
}
```

### Possibilité 2 : Modifier la rétention
```python
# Dans jobs_config.py
DATA_RETENTION_DAYS = 7   # Garder 1 semaine seulement
# ou
DATA_RETENTION_DAYS = 60  # Garder 2 mois
```

### Possibilité 3 : Filtrer par salaire/state dans Google Sheets
```
Utilise les filtres natifs de Sheets sur les colonnes !
```

---

## 📋 Fichiers Modifiés

```
✅ jobs_config.py       (NOUVEAU - Configuration centralisée)
✅ data_cleaner.py      (NOUVEAU - Nettoyage automatique)
✅ seek_scraper.py      (REFACTORISÉ - Multi-catégorie)
✅ .github/workflows/scrape.yml (AMÉLIORÉ - Multi-category)
✅ GitHub repo          (POUSSÉ - Prêt à tourner)
```

---

## ✨ Résumé Ultime

**Avant :** Scrape juste les "labourer" du Queensland
**Maintenant :** Scrape 10 catégories × 8 états automatiquement ! 🎉

**Avant :** CSV devient énorme avec du vieux contenu
**Maintenant :** Auto-nettoyage après 30 jours ✨

**Avant :** Besoin de maintenance manuelle
**Maintenant :** Complètement automatique 24h/24 🤖

---

## 🎓 Comment ça tourne ?

1. **GitHub Actions** exécute le scraper toutes les 2 heures
2. **Scraper** boucle sur 10 catégories × 8 états
3. **Seek.com.au** renvoie les résultats
4. **CSV** se remplit avec les nouvelles offres
5. **Data Cleaner** archive les vieilles (> 30 jours)
6. **GitHub** sauvegarde tout
7. **Google Sheets** se met à jour via l'import URL

---

## 🎉 C'EST FAIT !

Ton scraper multi-catégorie tourne maintenant sur GitHub !

**Prochainement : centaines de jobs d'Australie dans ton CSV ! 📊🚀**
