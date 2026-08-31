# TARDIS — Predicting the Unpredictable

Projet Epitech (G-AIA-210). Analyse des retards de trains SNCF et prediction
des retards via un modele de machine learning, presente dans un dashboard
Streamlit interactif.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

1. **Nettoyage & analyse** : ouvrir et executer `notebooks/tardis_eda.ipynb`
   (lit `dataset.csv`, genere `cleaned_dataset.csv`).
2. **Modele** : ouvrir et executer `notebooks/tardis_model.ipynb`
   (lit `cleaned_dataset.csv`, genere `model.joblib`).
3. **Dashboard** :

```bash
streamlit run tardis_dashboard.py
```

<!-- TODO (etape 4) : detailler les fonctionnalites du dashboard -->

## Structure du repo

```
├── dataset.csv            # donnees brutes (entree, ne pas modifier)
├── notebooks/
│   ├── tardis_eda.ipynb   # etapes 1-2 : nettoyage + analyse exploratoire
│   └── tardis_model.ipynb # etape 3 : entrainement et selection du modele
├── cleaned_dataset.csv    # genere par tardis_eda.ipynb
├── model.joblib           # genere par tardis_model.ipynb
├── tardis_dashboard.py    # etape 4 : dashboard Streamlit
├── utils/                 # fonctions partagees (nettoyage, features)
├── docs/                  # memo d'organisation de l'equipe
└── requirements.txt
```

## Coding style

Le projet est formate avec [ruff](https://docs.astral.sh/ruff/) :

```bash
ruff format .    # avant chaque push (verifie par le CI)
```

## Equipe

<!-- TODO : noms des 3 membres -->
