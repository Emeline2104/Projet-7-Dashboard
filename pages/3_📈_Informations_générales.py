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
import matplotlib.pyplot as plt
import seaborn as sns

# Environnement local
api_url = "http://127.0.0.1:5001"
# Environnement Heroku
# api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')

# Récupère l'ID client de la session state
client_id = st.session_state.client_id
client_info = st.session_state.client_info
application_info = client_info['informations_application'][0]
st.title("Page d'informations générales")

# Ajoutez une fonction pour obtenir les informations du groupe pour la comparaison
def get_group_info_for_comparison(filters):
    api_url = 'http://127.0.0.1:5001/get_group_info'
    response = requests.get(api_url, params=filters)
    group_info = response.json()
    return group_info

def determine_age_group(age):
    if -(age/365) < 30:
        return 'Moins de 30 ans'
    elif -(age/365) <= age < 40:
        return '30-40 ans'
    elif -(age/365) <= age < 50:
        return '40-50 ans'
    else:
        return 'Plus de 50 ans'

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
            group_info_for_comparison = get_group_info_for_comparison(filters)
            group_info_for_comparison = json.loads(group_info_for_comparison)

            # Calcul de la moyenne des cibles pour les clients
            average_target_individual = sum(entry['TARGET'] for entry in group_info_for_comparison) / len(group_info_for_comparison)

            # Graphique 1 : Comparaison des probabilités de défaut de prêt
            fig, ax = plt.subplots()
            target_client = application_info['TARGET']
            custom_palette = sns.color_palette(['#c44e52', '#55a868'])
            colors = [custom_palette[0] if target_client > 0.15 else custom_palette[1],
                      custom_palette[0] if average_target_individual > 0.15 else custom_palette[1]]

            sns.barplot(x=['Client', 'Moyenne pour les individus'], y=[target_client, average_target_individual], ax=ax, palette=colors)

            for i, value in enumerate([target_client, average_target_individual]):
                ax.text(i, value, f'{value:.2f}', ha='center', va='bottom' if value > 0 else 'top', fontsize=10, color='black')

            ax.set_ylabel('Moyenne des probabilités de défaut de prêt')
            ax.set_title('Comparaison des probabilités de défaut de prêt du client et des individus de comparaison')

            # Afficher le graphique dans Streamlit
            st.pyplot(fig)

            # Graphique 2 : Comparaison des montants de demande de crédit
            average_amt_credit_individual = sum(entry['AMT_CREDIT'] for entry in group_info_for_comparison) / len(group_info_for_comparison)
            fig, ax = plt.subplots()
            amt_credit_client = application_info['AMT_CREDIT']

            sns.barplot(x=['Client', 'Moyenne pour les individus'], y=[amt_credit_client, average_amt_credit_individual], ax=ax, palette=colors)

            for i, value in enumerate([amt_credit_client, average_amt_credit_individual]):
                ax.text(i, value, f'{value:.0f} €', ha='center', va='bottom' if value > 0 else 'top', fontsize=10, color='black')

            ax.set_ylabel('Moyenne des montants de demande de crédit')
            ax.set_title('Comparaison des montants de prêt du client et des individus de comparaison')

            # Afficher le graphique dans Streamlit
            st.pyplot(fig)

            # Graphique 3 : Comparaison des montants des annuités de crédit
            amt_annuity_values = [entry['AMT_ANNUITY'] for entry in group_info_for_comparison if entry['AMT_ANNUITY'] is not None]
            average_amt_annuity_individual = sum(amt_annuity_values) / len(amt_annuity_values)

            fig, ax = plt.subplots()
            amt_annuity_client = application_info['AMT_ANNUITY']

            sns.barplot(x=['Client', 'Moyenne pour les individus'], y=[amt_annuity_client, average_amt_annuity_individual], ax=ax, palette=colors)

            for i, value in enumerate([amt_annuity_client, average_amt_annuity_individual]):
                ax.text(i, value, f'{value:.0f} €', ha='center', va='bottom' if value > 0 else 'top', fontsize=10, color='black')

            ax.set_ylabel('Moyenne des montants des annuités de crédit')
            ax.set_title('Comparaison des annuités de prêt du client et des individus de comparaison')
            
            # Afficher le graphique dans Streamlit
            st.pyplot(fig)

    except Exception as e:
        st.json({'error': str(e), 'status_code': 500})