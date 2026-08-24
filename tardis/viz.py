"""Helpers de visualisation partages entre le notebook EDA et le dashboard.

Regle d'equipe : un graphique utilise a la fois dans le notebook et dans le
dashboard est defini ici, pas duplique. Chaque fonction retourne une figure
matplotlib et n'appelle jamais plt.show() : c'est a l'appelant d'afficher
(plt.show() en notebook, st.pyplot() en Streamlit).
"""

import matplotlib.pyplot as plt

from tardis import config


def delay_distribution(df, column=None, bins=50):
    """Histogramme de la distribution des retards.

    TODO :
        tracer un hist de df[column]
        marquer la mediane par une ligne verticale
        couper l'axe x aux percentiles 1-99 : quelques valeurs extremes
        ecrasent sinon toute la distribution
    """
    column = column or config.TARGET
    fig, ax = plt.subplots()
    ax.set_title(f"Distribution : {column}")
    _ = bins
    return fig


def delay_by_station(df, top_n=15):
    """Barres horizontales des N gares les plus en retard.

    TODO :
        grouper par gare de depart, moyenne de la cible
        garder les gares avec assez d'observations (sinon une gare a 2 lignes
        remonte en tete du classement par pur hasard)
        trier, garder top_n, barres horizontales
    """
    fig, ax = plt.subplots()
    ax.set_title(f"Top {top_n} gares par retard moyen")
    _ = df
    return fig


def delay_over_time(df, route=None):
    """Serie temporelle du retard moyen, globale ou pour un trajet.

    TODO :
        filtrer sur la route si fournie
        grouper par mois, moyenne de la cible
        courbe + moyenne mobile 3 mois pour lisser
    """
    fig, ax = plt.subplots()
    ax.set_title(f"Evolution du retard{f' : {route}' if route else ''}")
    _ = df
    return fig


def correlation_heatmap(df, columns=None):
    """Matrice de correlation des variables numeriques.

    TODO :
        selectionner les colonnes numeriques
        df.corr(), imshow avec une palette divergente centree sur 0
        annoter les cases, faire pivoter les labels
    """
    fig, ax = plt.subplots()
    ax.set_title("Correlations")
    _ = (df, columns)
    return fig
