# TARDIS — Predicting the unpredictable

Analyse des retards de trains SNCF, modele de prediction et dashboard
interactif. Projet EPITECH G-AIA-210.

## Equipe

| Membre | Perimetre |
|---|---|
| _(nom)_ | Nettoyage + EDA — `tardis/cleaning.py`, `tardis_eda.ipynb` |
| _(nom)_ | Features + modele — `tardis/features.py`, `tardis_model.ipynb` |
| _(nom)_ | Dashboard + CI — `tardis/viz.py`, `tardis_dashboard.py`, `.github/` |

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Le dataset brut doit s'appeler **`dataset.csv`** a la racine : c'est le nom
utilise par les tests automatises du sujet.

## Utilisation

```bash
# 1. Nettoyage et exploration -> produit cleaned_dataset.csv
jupyter notebook tardis_eda.ipynb

# 2. Entrainement -> produit model.joblib
jupyter notebook tardis_model.ipynb

# 3. Dashboard
streamlit run tardis_dashboard.py
```

## Structure

```
.
├── dataset.csv               # brut (nom impose par le sujet)
├── cleaned_dataset.csv       # genere par tardis_eda.ipynb
├── model.joblib              # genere par tardis_model.ipynb
├── tardis_eda.ipynb          # etapes 1 & 2 : nettoyage, EDA
├── tardis_model.ipynb        # etape 3 : modelisation
├── tardis_dashboard.py       # etape 4 : Streamlit
├── tardis/                   # code partage — la source de verite
│   ├── config.py             # chemins, colonnes, cible, colonnes fuitantes
│   ├── cleaning.py           # parsing et normalisation du brut
│   ├── features.py           # feature engineering
│   └── viz.py                # graphiques partages notebook/dashboard
├── tests/                    # tests unitaires du code partage
├── requirements.txt
└── ruff.toml                 # coding style impose
```

**Regle d'equipe :** toute logique utilisee a plus d'un endroit vit dans
`tardis/`. Les notebooks appellent, ils ne reimplementent pas. C'est ce qui
evite que le dashboard nettoie les donnees differemment du notebook.

## Le dataset en une phrase

Une ligne = **un trajet (origine-destination) sur un mois donne**, pas un
train. Environ 12 000 lignes, de janvier 2018 a octobre 2025, ~130 gares.

Conséquence directe : « heure de depart », « heure de pointe » et « jour de la
semaine », cites en exemple par le sujet, **n'existent pas** dans ces donnees.
La granularite temporelle s'arrete au mois.

Le brut est volontairement sale :

| Probleme | Exemple |
|---|---|
| 5 formats de date | `2018-01`, `2018 01`, `2018/01`, `01-2018`, `2018-01 ` |
| Virgule decimale | `5,04` |
| Unites collees | `6.7 min`, `9.52%` |
| Casse et espaces | `paris lyon`, ` ANNECY ` |
| Alias de gares | `ANGERS ST LAUD` vs `ANGERS SAINT LAUD` |
| Valeur parasite | gare = `0` |
| Doublons | 174 stricts, 223 sur (date, depart, arrivee) |
| Valeurs manquantes | ~240 par colonne |
| Incoherences metier | annules > programmes, comptages negatifs |

## Cible et fuite de donnees

**Cible :** `Average delay of all trains at arrival` (minutes).

Les colonnes listees dans `config.LEAKY_COLUMNS` sont mesurees **en meme temps
que la cible**. Les inclure dans les features donne un R² proche de 1 qui ne
prouve rien. C'est le principal piege du sujet.

## Coding style

```bash
ruff format .        # formate
ruff format --check .  # verifie (ce que fait la CI)
ruff check .         # lint
pytest -q tests      # tests unitaires
```

## Workflow git

Personne ne pousse sur `main`. Une branche par tache, une PR, une relecture
par un autre membre.

```bash
git switch -c feat/cleaning-dates
# ... travail ...
ruff format . && pytest -q tests
git push -u origin feat/cleaning-dates
```

Prefixe `no-ga/` sur une branche pour pousser sans declencher la CI.

### Conflits sur les notebooks

Un `.ipynb` est un JSON contenant les sorties : deux personnes qui touchent le
meme notebook produisent un conflit illisible. D'ou la regle : **un notebook,
un responsable**. Le code partage passe par `tardis/`, ou les conflits sont
lisibles.

## CI

Definie dans `.github/workflows/tardis.yml`, declenchee sur push et sur PR.

| Job | Role |
|---|---|
| `guard` | Coupe la CI sur les branches `no-ga/*` et sur le miroir ; detecte notebooks, tests et dataset |
| `coding_style` | `ruff format --check` (bloquant) + `ruff check` (annotations) |
| `deliverables` | Presence des fichiers imposes, validite JSON des notebooks |
| `tests` | `pytest` — saute automatiquement si `tests/` est absent |
| `notebooks` | Execute chaque notebook, un job parallele par notebook |
| `dashboard` | Demarre Streamlit et interroge `/_stcore/health` |
| `verdict` | Agrege tout — la seule check a proteger sur `main` |
| `push_to_mirror` | Miroir Epitech, uniquement sur push |

Variables a ajuster en tete de fichier : `MIRROR_SSH_URL` (obligatoire),
`RUN_NOTEBOOKS` et `RUFF_LINT_STRICT` (a passer a `true` en fin de projet).

Secret requis : `GIT_SSH_PRIVATE_KEY` — la cle **privee**, pas la publique.
