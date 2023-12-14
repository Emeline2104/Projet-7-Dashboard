# Recherche_client.py
import streamlit as st
import requests

# Modifie l'URL de l'API en fonction de l'environnement (local ou Heroku)

# Environnement local
api_url = "http://127.0.0.1:5001"
# Environnement Heroku
#api_url = "https://projet-7-38cdf763d118.herokuapp.com/"


# Page d'accueil
st.title("Bienvenue sur le tableau de bord")
st.markdown(
    """
    Bienvenue dans le tableau de bord interactif de Prêt à Dépenser. 
    Les onglets sont disposés de la manière suivante : 

    - **Informations Client**
    - **Informations sur la Demande de Crédit**
    - **Informations Générales sur les Demandes de Crédit**
    """
)
st.header("Entrez l'identifiant du client pour obtenir des information:")


client_id = st.text_input("ID du client:")
st.session_state.client_id = client_id

if st.button("Valider et accéder aux informations du client"):
    response = requests.get(f"{api_url}/informations_client_brut/{client_id}")
    client_info = response.json()
    st.session_state.client_info = client_info
    # Redirige l'utilisateur vers la page d'informations client
    st.session_state.page = "1_📊_Informations_client"
else:
    # Initialisation par défaut si le bouton n'est pas encore cliqué
    st.session_state.client_info = {}
# To do : ajouter une requete pour vérifier que l'ID client est bien dedans et sinon erreur