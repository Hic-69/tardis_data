"""Constantes partagees par les notebooks, le dashboard et les tests.

Tout ce qui est un chemin, un nom de colonne ou un seuil vit ici. Regle
d'equipe : aucune chaine de caracteres en dur ailleurs dans le projet.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAW_DATASET = ROOT / "dataset.csv"
CLEAN_DATASET = ROOT / "cleaned_dataset.csv"
MODEL_PATH = ROOT / "model.joblib"

CSV_SEPARATOR = ";"

# --- Colonnes du dataset brut ------------------------------------------------

COL_DATE = "Date"
COL_SERVICE = "Service"
COL_DEPARTURE = "Departure station"
COL_ARRIVAL = "Arrival station"
COL_JOURNEY_TIME = "Average journey time"
COL_SCHEDULED = "Number of scheduled trains"
COL_CANCELLED = "Number of cancelled trains"

# Colonnes textuelles libres : lourdes, jamais utilisees comme features.
COMMENT_COLUMNS = [
    "Cancellation comments",
    "Departure delay comments",
    "Arrival delay comments",
]

IDENTIFIER_COLUMNS = [COL_DATE, COL_SERVICE, COL_DEPARTURE, COL_ARRIVAL]

# --- Cible de prediction -----------------------------------------------------

# Le retard moyen a l'arrivee, tous trains confondus : c'est la variable que
# le sujet appelle "delay duration in minutes".
TARGET = "Average delay of all trains at arrival"

# ATTENTION FUITE DE DONNEES (data leakage).
# Ces colonnes sont mesurees EN MEME TEMPS que la cible : les donner au modele
# revient a lui donner la reponse. Elles sont exclues des features.
LEAKY_COLUMNS = [
    "Number of trains delayed at arrival",
    "Average delay of late trains at arrival",
    "Number of trains delayed > 15min",
    "Average delay of trains > 15min (if competing with flights)",
    "Number of trains delayed > 30min",
    "Number of trains delayed > 60min",
    "Number of trains delayed at departure",
    "Average delay of late trains at departure",
    "Average delay of all trains at departure",
    "Pct delay due to external causes",
    "Pct delay due to infrastructure",
    "Pct delay due to traffic management",
    "Pct delay due to rolling stock",
    "Pct delay due to station management and equipment reuse",
    "Pct delay due to passenger handling (crowding, disabled persons, connections)",
]

# --- Nettoyage ---------------------------------------------------------------

# Formats de date presents dans le brut (2018-01, 2018 01, 2018/01, 01-2018...)
DATE_FORMATS = ["%Y-%m", "%Y %m", "%Y/%m", "%m-%Y", "%m/%Y", "%m %Y"]

# Valeurs de gare qui ne sont pas des gares.
STATION_JUNK = {"0", "", "NAN", "NONE", "N/A", "-"}

# Alias de gares vus dans le brut (variantes d'orthographe).
STATION_ALIASES = {
    "ANGERS ST LAUD": "ANGERS SAINT LAUD",
    "PARIS MONTPARNASSE 1 ET 2": "PARIS MONTPARNASSE",
    "ST PIERRE DES CORPS": "SAINT PIERRE DES CORPS",
    "ST ETIENNE CHATEAUCREUX": "SAINT ETIENNE CHATEAUCREUX",
    "ST MALO": "SAINT MALO",
}
