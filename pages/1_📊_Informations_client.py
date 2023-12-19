"""
Script 1_📊_Informations_client.py

Ce script Streamlit permet d'afficher les informations sur un client à partir d'un ID client spécifié.

Le script utilise des fonctions pour organiser l'affichage des informations, notamment sur les informations
personnelles, les données du bureau, et les demandes précédentes. Des listes déroulantes permettent de choisir
les informations à afficher, et des expander sont utilisés pour afficher des informations supplémentaires.

Le script utilise un environnement local par défaut, mais la variable `api_url` peut être modifiée pour l'environnement
Heroku.

Remarques:
- Assurez-vous d'avoir les dépendances requises installées en exécutant : pip install requirements.txt.
- Pour personnaliser l'environnement, modifiez l'URL de l'API en décommentant l'environnement souhaité.
"""

import streamlit as st
import requests
from Data.config import (
    correspondance_dict_application_info,
    correspondance_dict_bureau_info,
    correspondance_dict_previous_application_info
)


# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')

# Récupération de l'ID client de la session state
client_id = st.session_state.client_id
client_info = st.session_state.client_info

def afficher_informations_client(client_id):
    """
    Fonction pour afficher les informations sur le client.

    Parameters:
    - client_id (str): L'ID du client.

    """
    st.title("Page d'informations sur le client")
    st.write(f"**ID du client :** {client_id}")

    try:
        afficher_informations_application(client_info.get('informations_application', [])[0])
        afficher_informations_bureau(client_info.get('informations_bureau', [])[0])
        afficher_informations_previous_application(client_info.get('informations_previous_application', [])[0])

    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

def afficher_informations_generales(titre, info, correspondance_dict):
    """
    Fonction générique pour afficher les informations.

    Parameters:
    - titre (str): Le titre de la section.
    - info (dict): Les informations spécifiques à afficher.
    - correspondance_dict (dict): Le dictionnaire de correspondance des informations.

    """
    st.subheader(titre)

    titres_informations = [correspondance_dict[key]['Titre'] for key in correspondance_dict.keys()]
    choix_information = st.selectbox("Choisir une information:", titres_informations)

    for key, value in correspondance_dict.items():
        if value['Titre'] == choix_information:
            cle_correspondante = key
            break

    st.write(f"Valeur : {info[cle_correspondante]}")
    st.write(f"Unité : {value.get('Unité', 'Aucune unité disponible')}")
    st.write(f"Description : {value.get('Description', 'Aucune description disponible')}")

def afficher_informations_application(application_info):
    """
    Fonction pour afficher les informations sur l'application.

    Parameters:
    - application_info (dict): Les informations sur l'application du client.

    """
    afficher_informations_generales("Informations personnelles:", application_info, correspondance_dict_application_info)

def afficher_informations_bureau(bureau_info):
    """
    Fonction pour afficher les informations sur le bureau.

    Parameters:
    - bureau_info (dict): Les informations sur le bureau du client.

    """
    afficher_informations_generales("Informations concernant les données des institutions financières:", bureau_info, correspondance_dict_bureau_info)

def afficher_informations_previous_application(previous_application_info):
    """
    Fonction pour afficher les informations sur les demandes précédentes.

    Parameters:
    - previous_application_info (dict): Les informations sur les demandes précédentes du client.

    """
    afficher_informations_generales("Informations sur les anciennes demandes:", previous_application_info, correspondance_dict_previous_application_info)

def afficher_informations_pos_cash_balance(pos_cash_balance_info):
    """
    Fonction pour afficher les informations sur le POS_CASH_balance.

    Parameters:
    - pos_cash_balance_info (list): Les informations sur le POS_CASH_balance du client.

    """
    st.subheader("POS_CASH_balance_info:")
    for entry in pos_cash_balance_info:
        st.write(entry)

def afficher_informations_credit_card_balance(credit_card_balance_info):
    """
    Fonction pour afficher les informations sur les paiements par carte de crédit.

    Parameters:
    - credit_card_balance_info (dict): Les informations sur les paiements par carte de crédit du client.

    """
    st.subheader("Credit Card Balance Info:")
    st.write(credit_card_balance_info)

def afficher_informations_installments_payments(installments_payments_info):
    """
    Fonction pour afficher les informations sur les paiements d'acomptes.

    Parameters:
    - installments_payments_info (list): Les informations sur les paiements d'acomptes du client.

    """
    st.subheader("Installments Payments Info:")
    for entry in installments_payments_info:
        st.write(entry)

def afficher_informations_supplementaires(client_info):
    """
    Fonction pour afficher des informations supplémentaires dans une liste déroulante.

    Parameters:
    - client_info (dict): Les informations supplémentaires sur le client.

    """
    st.subheader("Informations supplémentaires:")
    with st.expander("Plus d'informations"):
        if 'POS_CASH_balance_info' in client_info:
            afficher_informations_pos_cash_balance(client_info['POS_CASH_balance_info'])
        if 'credit_card_balance_info' in client_info:
            afficher_informations_credit_card_balance(client_info['credit_card_balance_info'])
        if 'installments_payments_info' in client_info:
            afficher_informations_installments_payments(client_info['installments_payments_info'])

# Si l'ID client est défini, affiche les informations sur le client
if client_id:
    afficher_informations_client(client_id)
else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')
