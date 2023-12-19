"""
Script 3_📈_Informations_générales.py

Ce script Streamlit permet d'afficher des informations générales sur un client et de comparer ces informations
avec celles du groupe en fonction de différents filtres tels que l'âge, le genre et le type d'emploi.

Prérequis :
- Streamlit doit être installé : pip install streamlit
- Requests doit être installé : pip install requests
- Matplotlib doit être installé : pip install matplotlib
- Seaborn doit être installé : pip install seaborn

"""

import streamlit as st
import requests
import json
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Environnement local
api_url = "http://127.0.0.1:5001"
# Environnement Heroku
# api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')
else : 
    # Récupère l'ID client de la session state
    client_id = st.session_state.client_id
    client_info = st.session_state.client_info
    client_features = st.session_state.client_features
    application_info = client_info['informations_application'][0]
    application_train_test = st.session_state.application_train_test
st.title("Page d'informations générales")

def determine_age_group(age):
    if -(age/365) < 30:
        return 'Moins de 30 ans'
    elif -(age/365) <= age < 40:
        return '30-40 ans'
    elif -(age/365) <= age < 50:
        return '40-50 ans'
    else:
        return 'Plus de 50 ans'


# Ajoutez une fonction pour obtenir les informations du groupe pour la comparaison
def get_group_info_for_comparison(filters, application_train_test):
    filtered_data = application_train_test[['SK_ID_CURR', 'NAME_CONTRACT_TYPE', 'TARGET', 'DAYS_BIRTH', 'CODE_GENDER', 'OCCUPATION_TYPE', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_INCOME_TOTAL']]
    del application_train_test
    if 'age_group' in filters:
        filtered_data['AGE_GROUP'] = filtered_data['DAYS_BIRTH'].apply(determine_age_group)
        filtered_data = filtered_data[filtered_data['AGE_GROUP'] == filters['age_group']]
    if 'sex_filter' in filters:
        filtered_data = filtered_data[filtered_data['CODE_GENDER'] == filters['sex']]
    if 'job_filter' in filters:
        filtered_data = filtered_data[filtered_data['OCCUPATION_TYPE'] == filters['job']]
    # filtered_data_json = filtered_data.to_json(orient='records')
    return filtered_data

def determine_age_group(age):
    if -(age/365) < 30:
        return 'Moins de 30 ans'
    elif -(age/365) <= age < 40:
        return '30-40 ans'
    elif -(age/365) <= age < 50:
        return '40-50 ans'
    else:
        return 'Plus de 50 ans'

def get_global_feature_importance():
    # Appel de l'API pour obtenir l'importance globale des caractéristiques
    st.header("Caractéristiques principales du modèle:")
    response = requests.get(f"{api_url}/get_global_feature_importance")

    if response.status_code == 200:
        # Convertir la réponse JSON en DataFrame
        importance_df = pd.DataFrame(response.json())

        # Sélectionner les 20 caractéristiques les plus importantes
        top_features = importance_df.head(20)
        top_features = top_features[['Feature', 'Coefficient']]
        
        # Créer le graphique à barres avec Plotly
        fig = go.Figure()

        # Ajouter les barres avec la couleur grise
        fig.add_trace(go.Bar(
            x=top_features['Feature'],
            y=top_features['Coefficient'],
            marker_color='#808080',  # Couleur grise
        ))

        # Mise en forme du layout
        fig.update_layout(
            title='Top 20 des caractéristiques les plus importantes',
            yaxis_title='Coefficient',
            xaxis_title='Caractéristiques',
            barmode='relative',
        )

        # Ajuster la taille du graphique
        fig.update_layout(height=800)

        # Streamlit app
        st.plotly_chart(fig)

        st.markdown(
            """
            Le graphique affiche les 20 facteurs les plus influents selon le modèle.
            - Barres vers le haut : Impact positif. Par exemple, un revenu élevé favorise l'approbation du prêt.
            - Barres vers le bas : Impact négatif. Par exemple, un historique de crédit problématique peut diminuer la probabilité d'approbation.
            Explorez ces facteurs pour mieux comprendre comment le modèle prend ses décisions. 📊✨
            """)
    else:
        st.error(f"Erreur lors de la récupération de l'importance globale des caractéristiques : {response.status_code}")

def create_bar_chart(x, y, labels, title):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y, marker_color='#808080'))
    fig.update_layout(
        title=title,
        yaxis_title='Coefficient',
        xaxis_title='Caractéristiques',
        barmode='relative',
    )
    fig.update_layout(height=800)
    return fig

if client_info:
    try:
        # Interface utilisateur Streamlit
        comparison_mode = st.selectbox('Mode de comparaison', ['Ensemble du groupe', 'Par groupe d\'âge', 'Par genre', 'Par type d\'emploi'])

        if comparison_mode == 'Ensemble du groupe':
            filters = {}  # Pas de filtres supplémentaires
        elif comparison_mode == 'Par groupe d\'âge':
            age_filter = application_info['DAYS_BIRTH']
            age_group = determine_age_group(age_filter)
            filters = {'age_group': age_group}
        elif comparison_mode == 'Par genre':
            sex_filter = application_info['CODE_GENDER']
            filters = {'sex': sex_filter}
        elif comparison_mode == 'Par type d\'emploi':
            job_filter = application_info['OCCUPATION_TYPE']
            filters = {'job': job_filter}
        else:
            st.warning('Mode de comparaison non valide')

        # Bouton pour déclencher la comparaison
        if st.button('Comparer avec le groupe'):
            if comparison_mode == 'Par groupe d\'âge':
                st.write('Donnée associée du client:', filters['age_group'])
            elif comparison_mode == 'Par genre':
                st.write('Donnée associée du client:', filters['sex'])
            elif comparison_mode == 'Par type d\'emploi':
                st.write('Donnée associée du client:', filters['job'])

            # Obtenez les informations du groupe depuis l'API Flask en utilisant les filtres
            group_info_for_comparison = get_group_info_for_comparison(filters, application_train_test)
            del application_train_test
            # group_info_for_comparison = json.loads(group_info_for_comparison)
            # Calcul de la moyenne des cibles pour les clients
            average_target_individual = group_info_for_comparison['TARGET'].mean()
            target_client = application_info['TARGET']
            
            # Graphique 1 : Comparaison des probabilités de défaut de prêt
            fig = go.Figure()

            # Ajouter les barres avec la couleur grise
            fig.add_trace(go.Bar(
                x=['Client', 'Moyenne pour les individus'],
                y=[target_client, average_target_individual],
                marker_color=['firebrick', 'seagreen']
            ))

            # Mise en forme du layout
            fig.update_layout(
                title='Comparaison des probabilités de défaut de prêt du client et des individus de comparaison',
                yaxis_title='Moyenne des probabilités de défaut de prêt',
                xaxis_title='Groupe',
                barmode='relative',
            )

            # Ajuster la taille du graphique
            fig.update_layout(height=400)

            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig)

            # Graphique 2 : Comparaison des montants de demande de crédit
            average_amt_credit_individual = group_info_for_comparison['AMT_CREDIT'].mean()
            amt_credit_client = application_info['AMT_CREDIT']
        
            fig_credit_amounts_comparison = go.Figure()

            # Ajouter les barres avec la couleur grise
            fig_credit_amounts_comparison.add_trace(go.Bar(
                x=['Client', 'Moyenne pour les individus'],
                y=[amt_credit_client, average_amt_credit_individual],
                marker_color=['firebrick', 'seagreen']
            ))

            # Mise en forme du layout
            fig_credit_amounts_comparison.update_layout(
                title='Comparaison des montants de prêt du client et des individus de comparaison',
                yaxis_title='Moyenne des montants de demande de crédit',
                xaxis_title='Groupe',
                barmode='relative',
            )

            # Ajuster la taille du graphique
            fig_credit_amounts_comparison.update_layout(height=400)

            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig_credit_amounts_comparison)

            # Graphique 3 : Comparaison des montants des annuités de crédit
            average_amt_annuity_individual = group_info_for_comparison['AMT_ANNUITY'].mean()
            amt_annuity_client = application_info['AMT_ANNUITY']
            
            fig_annuity_amounts_comparison = go.Figure()

            # Ajouter les barres avec la couleur grise
            fig_annuity_amounts_comparison.add_trace(go.Bar(
                x=['Client', 'Moyenne pour les individus'],
                y=[amt_annuity_client, average_amt_annuity_individual],
                marker_color=['firebrick', 'seagreen']
            ))

            # Mise en forme du layout
            fig_annuity_amounts_comparison.update_layout(
                title='Comparaison des annuités de prêt du client et des individus de comparaison',
                yaxis_title='Moyenne des montants des annuités de crédit',
                xaxis_title='Groupe',
                barmode='relative',
            )

            # Ajuster la taille du graphique
            fig_annuity_amounts_comparison.update_layout(height=400)
            st.plotly_chart(fig_annuity_amounts_comparison)

            get_global_feature_importance()
    except Exception as e:
        st.json({'error': str(e), 'status_code': 500})
else : 
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')

