"""Feature engineering et construction de la matrice d'apprentissage.

Point de vigilance central du projet : le dataset est AGREGE PAR MOIS ET PAR
TRAJET. Une ligne n'est pas un train, c'est "tous les Bordeaux-Paris de
janvier 2018". Consequences directes :

- "heure de depart" et "heure de pointe", cites en exemple par le sujet,
  n'existent pas dans les donnees. Ne pas les inventer.
- "jour de la semaine" n'existe pas non plus. La granularite temporelle
  disponible s'arrete au mois.
- la cible est une MOYENNE de retard, pas le retard d'un train.

Ce que l'on peut reellement construire : des features de calendrier au mois,
l'identite du trajet, la charge de trafic, et l'historique du meme trajet.
"""

from tardis import config


def add_temporal_features(df):
    """Ajoute les features de calendrier derivees de la date.

    TODO :
        year       = date.dt.year
        month      = date.dt.month
        quarter    = date.dt.quarter
        is_summer  = month dans {7, 8}          (trafic vacances)
        is_winter  = month dans {12, 1, 2}      (meteo, greves de fin d'annee)

    Le mois est cyclique : decembre et janvier sont voisins, mais 12 et 1 sont
    eloignes numeriquement. Un modele lineaire s'y trompe. Encodage cyclique :
        month_sin = sin(2 * pi * month / 12)
        month_cos = cos(2 * pi * month / 12)
    Les modeles a arbres n'en ont pas besoin : a tester, et a justifier.
    """
    raise NotImplementedError


def add_route_features(df):
    """Ajoute les features liees au trajet lui-meme.

    TODO :
        route            = depart + " -> " + arrivee
        is_paris_origin  = la gare de depart contient "PARIS"
        is_paris_dest    = la gare d'arrivee contient "PARIS"
        is_international = service == "International"
        journey_time     = deja present (Average journey time)

    Piste : la duree du trajet est un proxy de la distance, donc du nombre
    d'occasions de prendre du retard. A verifier par la correlation.
    """
    raise NotImplementedError


def add_traffic_features(df):
    """Ajoute les features de charge de trafic.

    TODO :
        cancellation_rate = annules / programmes        (garder la division
                                                         par zero a l'oeil)
        trains_per_day    = programmes / nb de jours du mois

    Attention : le taux d'annulation est-il connu AVANT le voyage ? Si le
    scenario d'usage est "predire le retard d'un trajet futur", non. A
    trancher en equipe et a assumer dans le notebook.
    """
    raise NotImplementedError


def add_lag_features(df):
    """Ajoute l'historique du meme trajet (features les plus predictives).

    TODO :
        trier par (route, date)
        pour chaque route :
            lag_1        = retard moyen du mois precedent
            rolling_3    = moyenne des 3 mois precedents
            route_mean   = moyenne historique de la route

    IMPERATIF : ne calculer ces moyennes que sur le PASSE (shift avant
    rolling). Utiliser le mois courant, c'est se donner la reponse.
    """
    raise NotImplementedError


def build_feature_matrix(df):
    """Assemble X et y prets pour scikit-learn.

    TODO :
        appliquer les quatre fonctions ci-dessus
        y = df[config.TARGET]
        supprimer les lignes ou y est NaN (on ne peut pas apprendre sans cible)
        X = df moins config.TARGET, config.LEAKY_COLUMNS, config.COMMENT_COLUMNS
        retourner X, y

    Le filtrage par config.LEAKY_COLUMNS n'est pas optionnel : sans lui, un
    R2 de 0.99 est garanti, et il ne veut rien dire.
    """
    _ = config.TARGET
    raise NotImplementedError


def build_preprocessor(numeric_features, categorical_features):
    """Construit le ColumnTransformer de preprocessing.

    TODO :
        numerique   : SimpleImputer(mediane) puis StandardScaler
        categoriel  : SimpleImputer(constante) puis OneHotEncoder(
                          handle_unknown="ignore")

    handle_unknown="ignore" est indispensable : une gare vue en test mais pas
    en entrainement ferait planter la prediction, et le dashboard avec elle.

    Emballer ca dans un Pipeline sklearn, pas dans des transformations
    manuelles : c'est ce pipeline complet qui sera serialise dans
    model.joblib, donc le dashboard n'aura aucun preprocessing a refaire.
    """
    raise NotImplementedError
