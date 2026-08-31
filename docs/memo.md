# MEMO — Projet TARDIS

## C'est quoi le projet ?

On fait partie d'un "SNCF Data Analysis Service". Le but : analyser les données
historiques de retards de trains, trouver des tendances, et construire un modèle
capable de **prédire le retard d'un train**. À la fin, tout sera présenté dans un
dashboard web interactif (Streamlit) — ça, c'est l'étape 4, on la fera ensemble après.

- **Langage** : Python (pandas, numpy, matplotlib, seaborn, scikit-learn)
- **Coding style** : tout le code doit passer `ruff format`
- **Dataset** : `dataset.csv` (données mensuelles de retards par trajet, volontairement sales)

---

## Étape 1 — Nettoyage du dataset

**Responsable :**___Axel___
**Date de rendu :** ___02/09/2026___

**Ce qu'il doit faire :**
- Charger et inspecter le dataset (attention : séparateur `;`)
- Supprimer les doublons
- Gérer les valeurs manquantes
- Corriger les valeurs sales : dates en plusieurs formats, noms de gares en
  majuscules/minuscules/avec espaces, nombres avec virgules, `min`, `%`...
- Convertir chaque colonne dans le bon type (dates, nombres, catégories)
- Créer de nouvelles variables utiles (mois, saison, trajet, taux de ponctualité...)

**Ce qu'il doit fournir :**
- `tardis_eda.ipynb` (partie nettoyage, avec explications dans le notebook)
- `cleaned_dataset.csv` (le dataset propre généré par le notebook)

---

## Étape 2 — Visualisation & analyse

**Responsable :** ___Foundhack___
**Date de rendu :** __03/09/2026__

**Ce qu'il doit faire :**
- Statistiques descriptives sur les variables clés (retard moyen, ponctualité...)
- Graphiques : distribution des retards, comparaison entre gares et trajets,
  évolution dans le temps, causes de retard, heatmap de corrélations
- Écrire une **interprétation en markdown sous chaque graphique** (les insights
  comptent autant que les graphes)

**Ce qu'il doit fournir :**
- La suite de `tardis_eda.ipynb` (même notebook que l'étape 1, section analyse)
- Minimum : distributions, comparaisons, corrélations + interprétations écrites

---

## Étape 3 — Modèle de prédiction

**Responsable :** ___Ash___
**Date de rendu :** __05/09/2026__

**Ce qu'il doit faire :**
- Construire un modèle de **régression** qui prédit le retard en minutes
  (cible : retard moyen à l'arrivée)
- Encoder les variables catégorielles (gares, service...) et préparer les features
- Entraîner **au moins 2-3 modèles** (un linéaire + des modèles à base d'arbres)
- Les comparer avec RMSE, MAE et R² — obligation de battre la baseline
  (prédire simplement la moyenne)
- Tuning d'hyperparamètres sur le meilleur modèle
- Justifier ses choix par écrit dans le notebook

**Ce qu'il doit fournir :**
- `tardis_model.ipynb` (entraînement, comparaison, tuning, justification)
- `model.joblib` (le modèle sauvegardé, utilisé ensuite par le dashboard)

---

## Fichiers finaux du repo (rappel)

| Fichier | Vient de |
|---|---|
| `requirements.txt` | tout le monde (dépendances du projet) |
| `tardis_eda.ipynb` | étapes 1 et 2 |
| `cleaned_dataset.csv` | étape 1 |
| `tardis_model.ipynb` | étape 3 |
| `model.joblib` | étape 3 |
| `tardis_dashboard.py` | étape 4 (à venir, ensemble) |
| `README.md` | étape 4 (installation + utilisation) |
