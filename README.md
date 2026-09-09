# TARDIS — Predicting the Unpredictable

Projet Epitech (G-AIA-210). Analyse des retards de trains SNCF et prediction
des retards via un modele de machine learning, presente dans un dashboard
Streamlit interactif.

## Arborescence

```
├── .github/
│   ├── CODEOWNERS
│   └── workflows/tardis.yml   # CI : ruff, pytest, mirroring Epitech
├── data/
│   └── dataset.csv            # dataset brut (entree, ne pas modifier)
├── docs/                      # memo d'organisation de l'equipe
├── notebooks/
│   ├── tardis_eda.ipynb       # etapes 1-2 : nettoyage + analyse exploratoire
│   └── tardis_model.ipynb     # etape 3 : entrainement et selection du modele
├── tests/
│   └── test_cleaned_dataset.py  # validation du fichier genere
├── cleaned_dataset.csv        # genere par tardis_eda.ipynb
├── model.pkl                  # genere par tardis_model.ipynb (a venir)
├── tardis_dashboard.py        # etape 4 : dashboard Streamlit (a venir)
├── README.md
└── requirements.txt
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Donnees

Le dataset brut est commite dans `data/dataset.csv` (separateur `;`).
Ne jamais le modifier a la main : tout le nettoyage vit dans les notebooks.

## Ordre d'execution

1. **Nettoyage & analyse** : executer `notebooks/tardis_eda.ipynb`
   — lit `data/dataset.csv`, genere `cleaned_dataset.csv` a la racine.
2. **Modele** : executer `notebooks/tardis_model.ipynb`
   — lit `cleaned_dataset.csv`, genere le modele sauvegarde.
3. **Dashboard** :

```bash
streamlit run tardis_dashboard.py
```

## Tests

Les tests valident le fichier genere `cleaned_dataset.csv` (pas le code des
notebooks). Si le fichier n'existe pas encore, ils sont sautes proprement.

```bash
pytest tests/
```

## Coding style

Le projet est formate avec [ruff](https://docs.astral.sh/ruff/) :

```bash
ruff format .    # avant chaque push (verifie par le CI)
ruff check .
```

## Equipe

<!-- TODO : noms des 3 membres -->
