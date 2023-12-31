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
# api_url = "http://127.0.0.1:5001"
# Environnement Heroku
api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None
    st.session_state.client_info = None
if 'client_features'not in st.session_state:
    st.session_state.client_features = None

# Récupère l'ID client de la session state
client_id = st.session_state.client_id
client_info = st.session_state.client_info
client_features = st.session_state.client_features

st.title("Page d'informations crédit")

@st.cache_data
def load_classification_threshold():
    """
    Charge le seuil de classification optimal à partir de l'API.

    Returns:
    - float: Le seuil de classification optimal.
             Retourne None en cas d'erreur lors de la requête.
    """
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
    - client_features (df): features du client.
    """
    # chargmenent du seuil de probabilité pour la classificatoin
    seuil_classification=load_classification_threshold()
    try:
        with st.spinner('Patientez un instant pour la prédiction ...'):
            response = requests.post(f"{api_url}/predict", json=client_features)

        if response.status_code == 200:
            predictions = response.json()
            st.session_state.target = predictions
            st.subheader("Prédictions pour le client:")
            
            # Verification de la structure de la réponse
            if 'prediction' in predictions and 'probability' in predictions:
                prediction_value = predictions['prediction']
                probability = predictions['probability']
                probability = round(probability, 4)

                if prediction_value == 1:
                    st.warning("Le client n'a pas obtenu son prêt.")
                else:
                    st.success("Le client a obtenu son prêt.")

                # Affichage des probabilités de prédiction
                st.write(f"**Probabilité de défaut du prêt** : {probability:.2f}")
                st.write(f"**Seuil maximal** : {seuil_classification:.2f}")
                st.write("*Probablité minimale au-delà duquel la demande de prêt est refusée.*")

                # Affichage de la jauge de probabilité
                couleur_jauge = "#800000" if probability > seuil_classification else "#006400"
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
    - client_info (dict): info du client.
    """
    st.subheader("Informations crédit:")
    try:
        if 'informations_application' in client_info:
            st.write(f"**Type de prêt:** {client_info['informations_application'][0]['NAME_CONTRACT_TYPE']}")
            st.write(f"**Montant du crédit demandé (€):** {client_info['informations_application'][0]['AMT_CREDIT']}")
            st.write(f"**Montant des annuités du crédit (€):** {client_info['informations_application'][0]['AMT_ANNUITY']}")
            st.write(f"**Montant des biens pour lequel le crédit est octroyé (€):** {client_info['informations_application'][0]['AMT_GOODS_PRICE']}")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
        
def visualize_top_features(client_features):
    """
    Visualise les caractéristiques les plus importantes pour la décision d'octroi de crédit.

    Parameters:
    - client_features (dict): Dictionnaire des caractéristiques du client.

    La fonction utilise une requête à une API pour obtenir les caractéristiques d'importance pour la prédiction
    d'octroi de crédit pour le client spécifié. Elle génère ensuite un graphique à barres interactif (utilisant
    Plotly) pour représenter visuellement les 20 caractéristiques les plus importantes.

    Le graphique présente les caractéristiques dans l'ordre décroissant de leur amplitude d'importance.
    Chaque barre du graphique représente une caractéristique particulière, et sa hauteur indique l'importance de
    cette caractéristique pour la décision du modèle. La couleur de la barre (rouge ou vert) indique la direction
    de l'impact de la caractéristique sur la probabilité d'octroi de crédit.

    """
    st.subheader("Explication des caractéristiques relatives au choix de l'octroi du prêt:")

    # Obtention des features importance locale à partir de l'API 
    with st.spinner('Patientez un instant pour l\'affichage des caractéristiques de la prédiction ...'):
        response = requests.post(f"{api_url}/get_importance-caracteristiques", json=client_features)
        
    if response.status_code == 200:
        # Extrais le contenu JSON de la réponse
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

        # Ajoute les barres pour les valeurs positives avec la couleur rouge
        fig.add_trace(go.Bar(
            x=top_features['Feature'],
            y=top_features['Importance'],
            marker_color=['#800000' if val > 0 else '#006400' for val in top_features['Importance']],  
            # Rouge pour les valeurs positives, vert pour les valeurs négatives
        ))

        # Mise en forme du layout
        fig.update_layout(
            title='Top 20 des caractéristiques les plus importantes',
            yaxis_title='Importance',
            xaxis_title='Caractéristiques',
            barmode='relative',
        )

        # Ajuste la taille du graphique
        fig.update_layout(height=800)

        # Streamlit app
        st.plotly_chart(fig)

        st.markdown(
            """
                Ce graphique explique la prédiction de défaut de crédit concernant le client spécifié. 
                Les caractéristiques qui ont le plus influencé la décision du modèle concernant la décision d'octroi du crédit. 
                - **Échelle de l'importance** : L'axe vertical représente l'importance de chaque caractéristique. Une barre plus haute signifie que cette caractéristique a une influence plus forte sur la décision du modèle.
                - **Caractéristiques individuelles** : Chaque barre sur le graphique correspond à une caractéristique particulière du client, comme le revenu, l'âge, ou le montant du prêt.
                - **Direction de l'impact** :  La direction de la barre indique si la caractéristique a une influence positive ou négative sur la probabilité de refus de crédit. 
                Une barre pointant vers le haut signifie une influence positive (rouge), et une barre pointant vers le bas signifie une influence négative (vert).
                - **Interprétation des barre** : En analysant ces barres, vous pouvez déterminer quelles caractéristiques ont le plus contribué à la probabilité de refus de crédit. 
                *Par exemple, si la barre la plus haute représente le revenu, cela signifie que le revenu a eu la plus grande influence sur la probabilité de refus.*
                
                En résumé, ce graphique aide à comprendre pourquoi le modèle a pris la décision qu'il a prise pour ce client spécifique. 
                Plus la barre est haute, plus la caractéristique est importante, et la direction de la barre indique si cette caractéristique a eu un impact positif ou négatif sur la probabilité de refus de crédit.
            """)
    else:
        st.error(f"Erreur lors de la récupération des caractéristiques d'importance : {response.status_code}")

# Si l'ID client est défini, affiche les informations sur le client
if client_id:
    make_predictions(client_features)
    afficher_informations_client(client_info)
    visualize_top_features(client_features)
else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')
