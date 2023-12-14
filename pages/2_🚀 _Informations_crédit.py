"""
Script 2_🚀_Informations_crédit.py

Ce script Streamlit permet d'afficher les informations sur un client et d'effectuer des prédictions de crédit.

Prérequis :
- Streamlit doit être installé : pip install streamlit

Le script utilise des fonctions pour organiser l'affichage des informations, notamment sur les prédictions de crédit
et les informations sur le client. Des prédictions sont effectuées en appelant une API, et les résultats sont affichés.

Le script utilise un environnement local par défaut, mais la variable `api_url` peut être modifiée pour l'environnement
Heroku.

"""

import streamlit as st
import requests
import math

# Environnement local
api_url = "http://127.0.0.1:5001"
# Environnement Heroku
# api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None

# Récupère l'ID client de la session state
client_id = st.session_state.client_id
client_info = st.session_state.client_info

st.title("Page d'informations crédit")

def make_predictions(client_id):
    """
    Fonction pour effectuer des prédictions de crédit.

    Parameters:
    - client_id (str): L'ID du client.

    """
    try:
        with st.spinner('Patientez un instant pour la prédiction ...'):
            response = requests.get(f"{api_url}/predict/{client_id}")

        if response.status_code == 200:
            predictions = response.json()
            st.session_state.target = predictions

            st.write("Prédictions pour le client :")
            if predictions['predictions'] == 1:
                st.warning("Le client n'a pas obtenu son prêt.")
            else:
                st.success("Le client a obtenu son prêt.")

        else:
            st.error("Erreur lors de l'effectuation des prédictions.")
    except Exception as e:
        st.error(f"Une erreur s'est produite lors des prédictions : {e}")

if client_id:
    make_predictions(client_id)
else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')

def afficher_informations_client(client_id):
    """
    Fonction pour afficher les informations sur le client.

    Parameters:
    - client_id (str): L'ID du client.

    """
    st.subheader("Informations crédit:")

    try:
        response = requests.get(f"{api_url}/informations_client_brut/{client_id}")
        client_info = response.json()

        st.session_state.client_info = client_info

        if 'informations_application' in client_info:
            afficher_informations_application(client_info['informations_application'][0])

    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

def afficher_informations_application(application_info):
    """
    Fonction pour afficher les informations sur l'application de crédit.

    Parameters:
    - application_info (dict): Les informations sur l'application de crédit du client.

    """
    st.write(f"**Type de prêt:** {application_info['NAME_CONTRACT_TYPE']}")
    st.write(f"**Genre du co-demandeur:** {application_info['NAME_CONTRACT_TYPE']}")
    st.write(f"**Âge du co-demandeur:** {application_info['DAYS_BIRTH']}")
    st.write(f"**Revenu annuel du co-demandeur (€):** {application_info['AMT_INCOME_TOTAL']}")

# Si l'ID client est défini, affiche les informations sur le client
if client_id:
    afficher_informations_client(client_id)
else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')
