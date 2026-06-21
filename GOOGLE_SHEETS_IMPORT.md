# 📊 Importer les données dans Google Sheets

## Vue d'ensemble

Tu as maintenant **4 fichiers CSV** générés automatiquement toutes les 2 heures :

```
Fichiers générés :
├─ jobs_australia_current.csv    → Jobs actuels (28K+)
├─ company_stats.csv             → Stats par compagnie
├─ location_stats.csv            → Stats par localisation
└─ category_stats.csv            → Stats par catégorie
```

Ces fichiers sont stockés sur **GitHub** dans le dossier `data/`.

---

## 🎯 Étape 1 : Créer un Google Sheet

1. Va sur [Google Sheets](https://sheets.google.com)
2. Crée un nouveau document : **+ Nouveau** → **Feuille de calcul**
3. Nomme-le : `Backpackers Jobs Australia`
4. Crée 4 onglets :
   - `Jobs Courant`
   - `Companies`
   - `Locations`
   - `Categories`

---

## 📥 Étape 2 : Importer les données via URLs

Pour chaque CSV, tu dois importer via une **URL brute GitHub**.

### Format URL brute GitHub

Pour un fichier à cette adresse :
```
https://github.com/USERNAME/REPO/blob/main/data/jobs_australia_current.csv
```

Remplace `/blob/` par `/raw/` :
```
https://github.com/USERNAME/REPO/raw/main/data/jobs_australia_current.csv
```

---

## 🔄 Importer dans Google Sheets

### Onglet 1 : Jobs Courant

1. Clique sur l'onglet `Jobs Courant`
2. **Données** → **Importer des données**
3. Sélectionne **Importer depuis l'URL**
4. Colle ton URL :
```
https://github.com/USERNAME/REPO/raw/main/data/jobs_australia_current.csv
```
5. Clique sur **Importer**
6. Choisis : **Remplacer les données à**
7. Sélectionne la cellule `A1` → **Importer**

✅ Les jobs s'importent automatiquement !

---

### Onglet 2 : Companies Stats

1. Clique sur l'onglet `Companies`
2. **Données** → **Importer des données**
3. **Importer depuis l'URL**
4. Colle :
```
https://github.com/USERNAME/REPO/raw/main/data/company_stats.csv
```
5. **Importer** → **Remplacer** → **A1**

Colonnes importées :
- `company` - Nom de la compagnie
- `state` - État
- `locations` - Localisations
- `job_categories` - Catégories de jobs
- `total_jobs` - Nombre total d'offres
- `avg_salary` - Salaire moyen
- `last_posted` - Dernière offre postée

---

### Onglet 3 : Location Stats

1. Clique sur l'onglet `Locations`
2. **Données** → **Importer des données**
3. **Importer depuis l'URL**
4. Colle :
```
https://github.com/USERNAME/REPO/raw/main/data/location_stats.csv
```
5. **Importer** → **Remplacer** → **A1**

Colonnes importées :
- `state` - État
- `location` - Localisation
- `total_jobs` - Nombre d'offres
- `top_category` - Catégorie la plus demandée
- `avg_salary` - Salaire moyen
- `last_posted` - Dernière offre

---

### Onglet 4 : Category Stats

1. Clique sur l'onglet `Categories`
2. **Données** → **Importer des données**
3. **Importer depuis l'URL**
4. Colle :
```
https://github.com/USERNAME/REPO/raw/main/data/category_stats.csv
```
5. **Importer** → **Remplacer** → **A1**

Colonnes importées :
- `job_category` - Catégorie (Construction, Hospitality, etc.)
- `total_jobs` - Nombre d'offres
- `avg_salary` - Salaire moyen
- `unique_companies` - Nombre de compagnies différentes
- `top_state` - État avec le plus de demande
- `demand_level` - Niveau de demande (HIGH, MEDIUM, LOW)

---

## ⏰ Mise à jour automatique

Les données se mettent à jour **automatiquement toutes les 2 heures** ! 

Google Sheets recharge l'URL toutes les heures par défaut. Ou tu peux forcer la mise à jour :

1. Va sur **Données** → **Plages importées**
2. Clique sur les 3 points → **Actualiser maintenant**

---

## 💡 Conseils

### Trier par demande
```
Onglet "Categories"
1. Sélectionne la colonne "total_jobs"
2. Données → Trier Z → A
→ Les jobs les plus demandés en haut !
```

### Filtrer par état
```
Onglet "Jobs Courant"
1. Clique sur une en-tête
2. Données → Créer un filtre
→ Filtre par "state" = "NSW", "VIC", etc.
```

### Graphiques
```
1. Sélectionne les données (ex: job_category + total_jobs)
2. Insertion → Graphique
3. Personnalise l'ordre, les couleurs, etc.
```

---

## 🚨 Troubleshooting

### "Erreur d'importation"
- ✅ Vérifie que ton repo est **public**
- ✅ Teste l'URL dans le navigateur (elle doit afficher le CSV)
- ✅ La première import peut prendre 2-3 min

### "Pas de données"
- ✅ Vérifie que le scraper a été exécuté (check GitHub Actions)
- ✅ Attends 2-3h après le lancement (première run)
- ✅ Regarde le fichier directement sur GitHub

### "Mise à jour ne fonctionne pas"
- ✅ Clique sur **Données** → **Plages importées** → Actualiser
- ✅ Google Sheets actualise toutes les heures
- ✅ Supprime et réimporte si c'est bloqué

---

## 📊 Exemple de résultat final

```
┌─────────────────────────────────────┐
│ Backpackers Jobs Australia          │
├─────────────────────────────────────┤
│ Jobs | Companies | Locations | ... │
└─────────────────────────────────────┘

Onglet "Jobs Courant":
  - 28,145 jobs actuels
  - Mise à jour : toutes les 2h
  - Filtrable par état, catégorie, salaire

Onglet "Companies":
  - Top embauche : "Heidrick & Struggles" (127 offres)
  - Salaire moyen : $72,000
  - États : NSW, VIC, QLD

Onglet "Locations":
  - Top demande : "Sydney NSW" (3,241 jobs)
  - Catégorie top : "Hospitality"
  - Salaire moyen : $65,000

Onglet "Categories":
  - TOP 3 demande : Hospitality (5,200), Warehouse (4,150), Security (3,890)
  - Demand Levels : HIGH (6 catégories), MEDIUM (3), LOW (1)
```

---

## ✨ Voilà !

T'as maintenant un **Google Sheet dynamique** qui se met à jour automatiquement avec les dernières données backpackers ! 🚀

L'accès est simple pour les backpackers :
- Ils voient les jobs à jour
- Ils visualisent les tendances par état/catégorie
- Ils savent où trouver le plus d'embauche
