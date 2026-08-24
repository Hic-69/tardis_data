"""TARDIS - dashboard Streamlit.

Lancement :
    streamlit run tardis_dashboard.py

Le dashboard doit demarrer meme si cleaned_dataset.csv ou model.joblib sont
absents : il affiche alors un avertissement au lieu de planter. C'est ce qui
permet au smoke test de la CI de valider le demarrage avant que les notebooks
aient produit leurs artefacts.
"""

import pandas as pd
import streamlit as st

from tardis import config

st.set_page_config(page_title="TARDIS", page_icon=":train:", layout="wide")


@st.cache_data
def load_data():
    """Charge le dataset nettoye. Retourne None s'il n'existe pas encore."""
    if not config.CLEAN_DATASET.exists():
        return None
    df = pd.read_csv(config.CLEAN_DATASET, parse_dates=[config.COL_DATE])
    return df


@st.cache_resource
def load_model():
    """Charge le pipeline sklearn serialise. Retourne None s'il est absent."""
    if not config.MODEL_PATH.exists():
        return None
    import joblib

    return joblib.load(config.MODEL_PATH)


def render_sidebar(df):
    """Filtres globaux appliques a tout le dashboard.

    TODO :
        selectbox gare de depart  (option "Toutes")
        selectbox gare d'arrivee  (dependante du depart choisi)
        slider de plage de dates
        multiselect du service (National / International)
        retourner le dataframe filtre
    """
    st.sidebar.header("Filtres")
    if df is None:
        st.sidebar.info("Aucune donnee chargee.")
        return df
    return df


def render_summary(df):
    """Panneau de statistiques cles - MUST HAVE du sujet.

    TODO : quatre st.metric cote a cote
        retard moyen a l'arrivee
        nombre total de trains programmes
        taux de ponctualite = 1 - (trains en retard / trains programmes)
        taux d'annulation
    """
    st.subheader("Vue d'ensemble")
    if df is None:
        st.warning("cleaned_dataset.csv est absent. Lance d'abord tardis_eda.ipynb.")
        return
    st.info("TODO : metriques cles")


def render_distribution(df):
    """Visualisation de la distribution des retards - MUST HAVE du sujet.

    TODO : viz.delay_distribution(df) puis st.pyplot(fig)
    """
    st.subheader("Distribution des retards")
    if df is None:
        return
    st.info("TODO : histogramme des retards")


def render_stations(df):
    """Comparaison des retards par gare - SHOULD HAVE du sujet.

    TODO : viz.delay_by_station(df) puis st.pyplot(fig)
    """
    st.subheader("Comparaison par gare")
    if df is None:
        return
    st.info("TODO : classement des gares")


def render_prediction(df, model):
    """Interface de prediction - MUST HAVE du sujet.

    TODO :
        formulaire : gare depart, gare arrivee, mois, annee, service,
                     duree de trajet estimee
        au clic :
            construire un dataframe d'UNE ligne avec exactement les memes
            colonnes que X a l'entrainement
            model.predict(row)
            afficher le resultat en st.metric, en minutes

    Piege classique : l'ordre et le nom des colonnes doivent correspondre a
    l'entrainement. Le plus simple est de serialiser la liste des colonnes
    avec le modele et de reconstruire la ligne depuis cette liste.
    """
    st.subheader("Predire un retard")
    if model is None:
        st.warning("model.joblib est absent. Lance d'abord tardis_model.ipynb.")
        return
    _ = df
    st.info("TODO : formulaire de prediction")


def main():
    st.title("TARDIS - Predicting the unpredictable")
    st.caption("Analyse et prediction des retards de trains SNCF")

    df = load_data()
    model = load_model()
    df = render_sidebar(df)

    render_summary(df)
    tab_explore, tab_predict = st.tabs(["Exploration", "Prediction"])
    with tab_explore:
        render_distribution(df)
        render_stations(df)
    with tab_predict:
        render_prediction(df, model)


if __name__ == "__main__":
    main()
