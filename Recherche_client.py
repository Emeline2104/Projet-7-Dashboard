"""
Tableau de Bord Streamlit - Prêt à Dépenser

Ce script Streamlit crée un tableau de bord interactif pour l'application Prêt à Dépenser. 
Il permet aux utilisateurs d'entrer l'identifiant d'un client pour obtenir 
des informations sur ce client, y compris des détails bruts provenant de différentes tables.

Auteur: Emeline Tapin
Date de création: 12/2023

Fonctions:
    - set_background_color(): Définit la couleur de fond de la page.
    - show_home_page(): Affiche la page d'accueil avec le titre et les informations générales.
    - read_data(file_path, chunk_size=2000000):
    Charge les données à partir d'un fichier CSV en utilisant un itérable de pandas.
    - replace_nan_with_none(d): Remplace les valeurs NaN d'un dictionnaire par None.
    - obtain_info_by_table(url, client_id):
    Obtient les informations d'une table spécifiée pour un client donné.
    - obtain_raw_client_data(client_id, data_reader): 
    Obtient les informations brutes sur un client spécifié à partir des différentes tables.
    - obtain_raw_client_info(client_id):
    Obtient les informations brutes sur un client spécifié à partir des différentes tables.
    - get_client_info(client_id, data):
    Récupère les informations sur un client spécifié à partir des données.
    - main(): Fonction principale qui crée et lance le tableau de bord.

Exécution:
    Exécutez le script en tant que programme principal pour lancer le tableau de bord Streamlit.

Note:
    Assurez-vous d'avoir installé toutes les dépendances nécessaires avant l'exécution.

"""
from Data.config import (
    APPLICATION_TRAIN_FILENAME,
    BUREAU_FILENAME,
    PREV_FILENAME,
    DATA_AGGREG_FILENAME,
)
import sys
import streamlit as st
import pandas as pd

def set_background_color():
    """
    Définit la couleur de fond de la page en utilisant du code HTML dans une balise style.
    """
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_home_page():
    """
    Affiche la page d'accueil avec le titre, l'image et les informations générales.
    """
    st.title("Bienvenue sur le tableau de bord")
    st.image("Capture d’écran 2023-12-14 à 18.38.41.png")
    st.markdown(
        """
        Bienvenue dans le tableau de bord interactif de Prêt à Dépenser. 
        Les onglets sont disposés de la manière suivante : 

        - **Informations client**
        - **Informations sur la demande de crédit**
        - **Informations de comparaison avec des groupes proches**
        - **Informations sur le modèle**
        """
    )
    st.header("Entrez l'identifiant du client pour obtenir des informations:")

@st.cache_data
def read_data(file_path, chunk_size=2000000):
    """
    Charge les données à partir d'un fichier CSV en utilisant un itérable de pandas.
    """
    data_reader = pd.read_csv(file_path, chunksize=chunk_size)
    data = pd.concat(data_reader)
    return data

def replace_nan_with_none(d):
    """
    Remplace les valeurs NaN d'un dictionnaire par None.
    """
    for key, value in d.items():
        if pd.isna(value):
            d[key] = None
    return d

def obtain_info_by_table(url, client_id):
    """
    Obtient les informations d'une table spécifiée pour un client donné.
    """
    informations_table = pd.read_csv(url)
    informations_table = informations_table[informations_table['SK_ID_CURR'] == client_id]
    return informations_table.to_dict(orient='records')

def obtain_raw_client_data(client_id):
    """
    Obtient les informations brutes sur un client spécifié à partir des différentes tables.
    """
    client_info = {}
    client_info['informations_application'] = obtain_info_by_table(
        APPLICATION_TRAIN_FILENAME, client_id)
    client_info['informations_bureau'] = obtain_info_by_table(
        BUREAU_FILENAME, client_id)
    client_info['informations_previous_application'] = obtain_info_by_table(
        PREV_FILENAME, client_id)
    return client_info

def obtain_raw_client_info(client_id):
    """
    Obtient les informations brutes sur un client spécifié à partir des différentes tables.
    """
    client_id = int(client_id)
    client_info = obtain_raw_client_data(client_id)
    return client_info

def get_client_info(client_id, data):
    """
    Récupère les informations sur un client spécifié à partir des données.
    """
    client_id = int(client_id)
    client_features = data[data['SK_ID_CURR'] == client_id].to_dict(orient='records')

    if client_features:
        client_data = replace_nan_with_none(client_features[0])
        st.session_state.client_features = client_data
        return client_data
    else:
        return {'error': 'Client non trouvé'}

def main():
    """
    Fonction principale pour exécuter le tableau de bord.

    - Configure la couleur de fond et affiche la page d'accueil.
    - Récupère l'ID du client à partir de l'entrée utilisateur.
    - Valide l'ID client et accède aux informations du client lorsqu'on appuie sur le bouton.
    - Affiche un message de succès et stocke les données en session state.

    """
    set_background_color()
    show_home_page()

    client_id = st.text_input("ID du client:")
    st.session_state.client_id = client_id

    if st.button("Valider et accéder aux informations du client"):
        with st.spinner('Patientez un instant pour le chargement des données ...'):
            client_info = obtain_raw_client_info(client_id)
            # Verification si le client n'a pas été trouvé dans la base de données
            if not any(client_info.values()):
                st.error("Client ID non trouvé dans la base de données, veuillez essayer avec un autre 'Client ID'.")
                sys.exit()
            st.session_state.client_info = client_info
            data = read_data(DATA_AGGREG_FILENAME)
            application_train_test = read_data(APPLICATION_TRAIN_FILENAME)
            st.session_state.application_train_test = application_train_test
            get_client_info(client_id, data)
        st.success('Vous pouvez accéder aux autres pages !')
    else:
        st.session_state.client_info = {}

if __name__ == "__main__":
    main()
