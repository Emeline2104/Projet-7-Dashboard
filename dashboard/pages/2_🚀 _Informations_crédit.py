# 2_🚀_Informations_crédit.py
import streamlit as st
import requests
import math 

# Environnement local
#api_url = "http://127.0.0.1:5001"
# Environnement Heroku
api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None

# Récupére l'ID client de la session state
client_id = st.session_state.client_id

st.title("Page d'informations crédit")

# Fonction pour effectuer des prédictions
def make_predictions(client_id):
    try:
        # Appelle l'API pour effectuer des prédictions
        response = requests.get(f"{api_url}/predict/{client_id}")

        # Vérifie si la réponse est réussie (code 200)
        if response.status_code == 200:
            # Affiche les prédictions
            predictions = response.json()
            st.write("Prédictions pour le client :")
            # Interprétation des prédictions
            if predictions['predictions'] == 1:
                st.warning("Le client n'a pas obtenu son prêt.")
            else:
                st.success("Le client a obtenu son prêt.")

        else:
            st.error("Erreur lors de l'effectuation des prédictions.")
    except Exception as e:
        st.error(f"Une erreur s'est produite lors des prédictions : {e}")

if client_id:
    response_target = requests.get(f"{api_url}/get_target/{client_id}")
    # Affiche la TARGET du client
    target_data = response_target.json()

    # Ajoute une nouvelle section pour indiquer si le client a obtenu son prêt ou non
    if 'TARGET' in target_data and not math.isnan(target_data['TARGET']):
        if target_data['TARGET'] == 1:
            st.warning("Le client n'a pas remboursé son prêt.")
        else:
            st.success("Le client a remboursé son prêt.")
    else:
        # Si la TARGET est NaN, effectue une prédiction et affiche les résultats
        make_predictions(client_id)
else : 
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')


# Fonction pour afficher les informations sur le client
def afficher_informations_client(client_id):
    st.subheader("Informations crédit:")

    try:
        # Affiche les informations sur le client
        response = requests.get(f"{api_url}/informations_client_brut/{client_id}") # à factoriser
        client_info = response.json()
        # Affiche les informations les plus importantes sur l'application
        if 'application_info' in client_info:
            afficher_informations_application(client_info['application_info'][0])

    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

# Fonction pour afficher les informations les plus importantes sur l'application
def afficher_informations_application(application_info):
    # Informations sur le crédit
    st.write(f"**Type de prêt:** {application_info['NAME_CONTRACT_TYPE']}")
    # st.write(f"**Statut du bien:** {application_info['NAME_YIELD_GROUP']}")
    # st.write(f"**Type de produit financier:** {application_info['NAME_PRODUCT_TYPE']}")
    # st.write(f"**Durée du prêt (années):** {application_info['TERM']}")
    # st.write(f"**Taux d'intérêt annuel (%):** {application_info['RATE_INTEREST_PRIVILEGED']}")
    #st.write(f"**Type de paiement:** {application_info['NAME_PAYMENT_TYPE']}")
    #st.write(f"**Type de garantie:** {application_info['NAME_TYPE_SUITE']}")

    # Informations sur le co-demandeur
    st.write(f"**Genre du co-demandeur:** {application_info['NAME_CONTRACT_TYPE']}")
    st.write(f"**Âge du co-demandeur:** {application_info['DAYS_BIRTH']}")
    st.write(f"**Revenu annuel du co-demandeur (€):** {application_info['AMT_INCOME_TOTAL']}")



# Si l'ID client est défini, affiche les informations sur le client
if client_id:
    afficher_informations_client(client_id)
else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')

# To do : ajouter l'analyse de la feature importance + factoriser les infos redondantes avec le 1er 