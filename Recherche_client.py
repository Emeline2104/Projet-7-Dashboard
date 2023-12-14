"""
Ce script implémente un tableau de bord interactif utilisant Streamlit pour afficher des informations sur les clients. Il se connecte à une API (environnement local ou Heroku) pour récupérer les données du client en fonction de l'identifiant fourni.

Usage:
1. Lancez le script pour exécuter le tableau de bord interactif.
2. Entrez l'identifiant du client pour obtenir des informations spécifiques.

Fonctions:
- set_background_color(): Définit la couleur de fond de la page en utilisant du code HTML.
- show_home_page(): Affiche la page d'accueil avec le titre, l'image et les informations générales.
- get_client_info(api_url, client_id): Récupère les informations du client en effectuant une requête à l'API.
- main(): Fonction principale qui organise l'exécution du programme.

Variables:
- api_url (str): L'URL de l'API en fonction de l'environnement (local ou Heroku).

Remarques:
- Assurez-vous d'avoir les dépendances requises installées en exécutant : pip install requirements.txt.
- Pour personnaliser l'environnement, modifiez l'URL de l'API en décommentant l'environnement souhaité.
"""

# Définir l'URL de l'API en fonction de l'environnement (local ou Heroku)
# Environnement local
api_url = "http://127.0.0.1:5001"
# Environnement Heroku
#api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

import streamlit as st
import requests

def set_background_color():
    """
    Définit la couleur de fond de la page en utilisant du code HTML dans une balise style.
    """
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0; /* Changer la couleur en gris (ou une autre couleur selon votre préférence) */
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
        - **Informations générales sur les demandes de crédit et comparaison avec des groupes proches**
        """
    )
    st.header("Entrez l'identifiant du client pour obtenir des informations:")

def get_client_info(api_url, client_id):
    """
    Récupère les informations du client en effectuant une requête à l'API en utilisant l'ID client fourni.

    Parameters:
    - api_url (str): L'URL de l'API.
    - client_id (str): L'identifiant du client.

    Returns:
    None
    """
    response = requests.get(f"{api_url}/informations_client_brut/{client_id}")
    client_info = response.json()
    st.session_state.client_info = client_info
    # Redirige l'utilisateur vers la page d'informations client
    st.session_state.page = "1_📊_Informations_client"


def main():
    """
    Fonction principale qui organise l'exécution du programme.
    """
    set_background_color()

    # Page d'accueil
    show_home_page()

    client_id = st.text_input("ID du client:")
    st.session_state.client_id = client_id

    if st.button("Valider et accéder aux informations du client"):
        with st.spinner('Patientez un instant pour le chargement des données ...'):
            get_client_info(api_url, client_id)
        st.success('Vous pouvez accéder aux autres pages !')

    else:
        # Initialisation par défaut si le bouton n'est pas encore cliqué
        st.session_state.client_info = {}

if __name__ == "__main__":
    main()