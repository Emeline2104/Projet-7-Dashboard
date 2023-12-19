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
import pandas as pd
import plotly.graph_objects as go

# Environnement local
api_url = "http://127.0.0.1:5001"
# Environnement Heroku
# api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None
    st.session_state.client_info = None
    st.session_state.client_features = None

# Récupère l'ID client de la session state
client_id = st.session_state.client_id
client_info = st.session_state.client_info
client_features = st.session_state.client_features

st.title("Page d'informations crédit")

def load_classification_threshold():
    # Chargement du seuil de classification optimal à partir du fichier texte
    response = requests.get(f"{api_url}/get_info_seuil")
    
    # Vérifie si la requête a réussi (statut 200 OK)
    if response.status_code == 200:
        # Extrais le contenu de la réponse et le convertis en float
        threshold = float(response.text)
        return threshold
    else:
        # Gére le cas où la requête a échoué
        print(f"Erreur lors de la requête : {response.status_code}")
        return None 

def make_predictions(client_features):
    """
    Fonction pour effectuer des prédictions de crédit.

    Parameters:
    - client_id (str): L'ID du client.
    - seuil_classification (float): Le seuil à partir duquel la classification est 0 ou 1.

    """
    seuil_classification=load_classification_threshold()
    try:
        with st.spinner('Patientez un instant pour la prédiction ...'):
            response = requests.post(f"{api_url}/predict", json=client_features)

        if response.status_code == 200:
            predictions = response.json()
            st.session_state.target = predictions

            st.subheader("Prédictions pour le client:")
            
            # Assurez-vous que la structure de la réponse est correcte
            if 'prediction' in predictions and 'probability' in predictions:
                prediction_value = predictions['prediction']
                probability = predictions['probability']
                probability = round(probability, 4)

                if prediction_value == 1:
                    st.warning("Le client n'a pas obtenu son prêt.")
                else:
                    st.success("Le client a obtenu son prêt.")

                # Affichez également les probabilités de prédiction
                st.write(f"**Probabilité de défaut du prêt** : {probability:.2f}")
                st.write(f"**Seuil maximal** : {seuil_classification:.2f}")
                st.write(f"*Probablité minimale au-delà duquel la demande de prêt est refusée.*")

                # Afficher la jauge de probabilité
                couleur_jauge = "#800000" if probability > seuil_classification else "#006400"

                # Configuration de la jauge Plotly
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Probabilité de défaut du prêt"},
                    gauge={
                        'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': couleur_jauge},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'threshold': {
                            'line': {'color': "black", 'width': 7},
                            'thickness': 1,
                            'value': seuil_classification}
                    }
                ))

                # Afficher la jauge Plotly
                st.plotly_chart(fig)

            else:
                st.error("Structure de réponse invalide.")
        else:
            st.error("Erreur lors de l'effectuation des prédictions.")
    except Exception as e:
        st.error(f"Une erreur s'est produite lors des prédictions : {e}")


def afficher_informations_client(client_info):
    """
    Fonction pour afficher les informations sur le client.

    Parameters:
    - client_id (str): L'ID du client.

    """
    st.subheader("Informations crédit:")

    try:
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
    st.write(f"**Revenu annuel du co-demandeur (€):** {application_info['AMT_INCOME_TOTAL']}")

def visualize_top_features(client_features):
    st.subheader("Explication des caractéristiques relatives au choix de l'octroi du prêt:")

    # Obtention des features importance locale à partir de l'API 
    with st.spinner('Patientez un instant pour l\'affichage des caractéristiques de la prédiction ...'):
        response = requests.post(f"{api_url}/get_importance-caracteristiques", json=client_features)

    if response.status_code == 200:
        # Extraire le contenu JSON de la réponse
        importance_dict = response.json()

        # Conversion du dictionnaire en DataFrame
        importance_df = pd.DataFrame(list(importance_dict.items()), columns=['Feature', 'Importance'])

        # Calcule l'amplitude des importances (valeur absolue)
        importance_df['Amplitude Importance'] = importance_df['Importance'].abs()

        # Trie le DataFrame par l'amplitude de l'importance en ordre décroissant et sélectionnez les 20 meilleures caractéristiques
        top_features = importance_df.sort_values(by='Amplitude Importance', ascending=False).head(20)
        top_features = top_features[['Importance', 'Feature']]
        # Créer le graphique à barres avec Plotly
        fig = go.Figure()

        # Ajouter les barres pour les valeurs positives avec la couleur rouge
        fig.add_trace(go.Bar(
            x=top_features['Feature'],
            y=top_features['Importance'],
            marker_color=['#800000' if val > 0 else '#006400' for val in top_features['Importance']],  # Rouge pour les valeurs positives, vert pour les valeurs négatives
        ))

        # Mise en forme du layout
        fig.update_layout(
            title='Top 20 des caractéristiques les plus importantes',
            yaxis_title='Importance',
            xaxis_title='Caractéristiques',
            barmode='relative',
        )

        # Ajuster la taille du graphique
        fig.update_layout(height=800)

        # Streamlit app
        st.plotly_chart(fig)

        st.markdown(
            """
            Ce graphique explique la prédiction de défaut de crédit concernant le client spécifié. 
            Les caractéristiques sont ordonnées en fonction de leur contribution à la prédiction, les caractéristiques en haut de la liste ayant l'impact le plus significatif.
            - Caractéristiques Positives : Les caractéristiques avec des barres orientées vers le haut ont une influence positive sur la prédiction. Une valeur plus élevée de ces caractéristiques accroît la probabilité de défaut de crédit, ce qui pourrait conduire au refus du crédit en raison d'un risque plus élevé.
            - Caractéristiques Négatives : Les caractéristiques avec des barres orientées vers le bas ont une influence négative. Une valeur plus élevée de ces caractéristiques diminue la probabilité de défaut de crédit, indiquant un risque moindre et favorisant l'approbation du crédit.)
            """
        )
    else:
        st.error(f"Erreur lors de la récupération des caractéristiques d'importance : {response.status_code}")

# Si l'ID client est défini, affiche les informations sur le client
if client_id:
    make_predictions(client_features)
    afficher_informations_client(client_info)
    visualize_top_features(client_features)
else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')
