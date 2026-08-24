"""Nettoyage du dataset brut SNCF.

Le brut est volontairement sale. Les saletes reperees, dans l'ordre ou ce
module les traite :

1. Dates en 5 formats melanges : "2018-01", "2018 01", "2018/01", "01-2018",
   et des variantes avec espace final.
2. Nombres stockes en texte : virgule decimale ("5,04"), suffixe d'unite
   ("6.7 min"), suffixe de pourcentage ("9.52%"), espaces autour.
3. Noms de gares incoherents : casse melangee, espaces en trop, alias
   ("ANGERS ST LAUD" vs "ANGERS SAINT LAUD"), et la valeur parasite "0".
4. Doublons stricts et doublons logiques sur (date, gare depart, gare arrivee).
5. Valeurs manquantes injectees dans toutes les colonnes.
6. Incoherences metier : retards moyens negatifs, comptages negatifs,
   trains annules > trains programmes.
"""

import re

import numpy as np
import pandas as pd

from tardis import config

_UNIT_SUFFIX = re.compile(r"\s*(min|minutes|%)\s*$", flags=re.IGNORECASE)


def load_raw(path=None):
    """Charge le CSV brut sans laisser pandas deviner les types.

    Tout est lu en texte : les colonnes numeriques contiennent des virgules
    decimales et des unites, un parsing automatique produirait des NaN
    silencieux.
    """
    path = path or config.RAW_DATASET
    return pd.read_csv(path, sep=config.CSV_SEPARATOR, dtype=str)


def to_numeric(series):
    """Convertit une colonne texte en float, en absorbant les saletes de format.

    "5,04" -> 5.04 | "6.7 min" -> 6.7 | "9.52%" -> 9.52 | " 6.51 " -> 6.51
    Tout ce qui reste illisible devient NaN.
    """
    cleaned = (
        series.astype("string")
        .str.strip()
        .str.replace(_UNIT_SUFFIX, "", regex=True)
        .str.replace(",", ".", regex=False)
        .str.replace(r"\s+", "", regex=True)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def parse_dates(series):
    """Parse la colonne Date malgre les formats melanges.

    Strategie : on essaie chaque format connu et on ne remplit que les trous
    laisses par les precedents. Plus lisible et plus sur qu'une regex unique.
    """
    raw = series.astype("string").str.strip()
    parsed = pd.Series(pd.NaT, index=raw.index, dtype="datetime64[ns]")
    for fmt in config.DATE_FORMATS:
        missing = parsed.isna()
        if not missing.any():
            break
        attempt = pd.to_datetime(raw[missing], format=fmt, errors="coerce")
        parsed.loc[missing] = attempt
    return parsed


def normalize_station(series):
    """Normalise les noms de gares : casse, espaces, alias, valeurs parasites."""
    normalized = (
        series.astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )
    normalized = normalized.replace(config.STATION_ALIASES)
    return normalized.where(~normalized.isin(config.STATION_JUNK), pd.NA)


def clean(df):
    """Pipeline de nettoyage complet : brut en texte -> dataframe type.

    Retourne un nouveau dataframe, ne modifie jamais celui recu.
    """
    out = df.copy()

    out[config.COL_DATE] = parse_dates(out[config.COL_DATE])
    for col in (config.COL_DEPARTURE, config.COL_ARRIVAL):
        out[col] = normalize_station(out[col])
    out[config.COL_SERVICE] = (
        out[config.COL_SERVICE].astype("string").str.strip().str.capitalize()
    )

    numeric_columns = [
        c
        for c in out.columns
        if c not in config.IDENTIFIER_COLUMNS and c not in config.COMMENT_COLUMNS
    ]
    for col in numeric_columns:
        out[col] = to_numeric(out[col])

    out = drop_duplicates(out)
    out = fix_business_rules(out)

    # Une ligne sans date ou sans trajet n'est identifiable par rien : elle
    # n'est reparable ni par imputation ni autrement.
    out = out.dropna(subset=[config.COL_DATE, config.COL_DEPARTURE, config.COL_ARRIVAL])
    return out.reset_index(drop=True)


def drop_duplicates(df):
    """Supprime les doublons stricts puis les doublons logiques.

    Doublon logique = meme mois + meme trajet. On garde la premiere occurrence,
    a discuter en equipe : agreger (moyenne ponderee) serait plus rigoureux.
    """
    out = df.drop_duplicates()
    key = [config.COL_DATE, config.COL_DEPARTURE, config.COL_ARRIVAL]
    return out.drop_duplicates(subset=key, keep="first")


def fix_business_rules(df):
    """Neutralise les valeurs metier impossibles.

    - un comptage de trains negatif n'existe pas -> NaN
    - annules > programmes est incoherent -> NaN sur les annules
    - un retard moyen tres negatif est une erreur de saisie -> NaN

    Un retard legerement negatif (train en avance) est plausible : le seuil
    est a -5 min, pas a 0.
    """
    out = df.copy()

    # On ne compare que ce qui est deja numerique : les colonnes de
    # commentaires contiennent le mot "delay" mais sont du texte libre.
    numeric = set(out.select_dtypes(include="number").columns)

    count_columns = [c for c in numeric if c.lower().startswith("number of")]
    for col in count_columns:
        out.loc[out[col] < 0, col] = np.nan

    if {config.COL_CANCELLED, config.COL_SCHEDULED} <= numeric:
        impossible = out[config.COL_CANCELLED] > out[config.COL_SCHEDULED]
        out.loc[impossible, config.COL_CANCELLED] = np.nan

    delay_columns = [
        c for c in numeric if "delay" in c.lower() and not c.startswith("Pct")
    ]
    for col in delay_columns:
        out.loc[out[col] < -5, col] = np.nan

    return out


def handle_missing(df):
    """Traite les valeurs manquantes restantes.

    TODO (a decider en equipe, et a JUSTIFIER dans le notebook) :

      pour chaque colonne numerique :
          si taux de NaN > 40 %      -> envisager de supprimer la colonne
          sinon si la colonne est la cible -> supprimer les lignes concernees
          sinon                      -> imputer par la mediane du couple
                                        (gare depart, gare arrivee), et a
                                        defaut par la mediane globale

    L'imputation par trajet bat l'imputation globale : Paris-Lyon et
    Paris-Brest n'ont pas du tout le meme profil de retard.
    """
    raise NotImplementedError("A implementer dans tardis_eda.ipynb")


def save_clean(df, path=None):
    """Ecrit le dataset nettoye au format attendu par le sujet."""
    path = path or config.CLEAN_DATASET
    df.to_csv(path, index=False)
    return path
