"""
Script 3_📈_Informations_comparaison.py

Ce script Streamlit permet de comparer les informations du client
avec celles du groupe en fonction de différents filtres tels que l'âge, le genre et le type d'emploi.
"""
from Data.config import correspondance_dict_application_info
import streamlit as st
import requests
import plotly.graph_objects as go

# Environnement local
# api_url = "http://127.0.0.1:5001"
# Environnement Heroku
api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

def determine_age_group(age):
    """
    Fonction auxiliaire pour déterminer la tranche d'âge en fonction de l'âge en jours.

    Args:
    - age (int): L'âge en jours.

    Returns:
    - str: La tranche d'âge correspondante.
    """
    if -(age/365) < 30:
        return 'Moins de 30 ans'
    elif -(age/365) <= age < 40:
        return '30-40 ans'
    elif -(age/365) <= age < 50:
        return '40-50 ans'
    else:
        return 'Plus de 50 ans'

def get_group_info_for_comparison(filters, application_train_test):
    """
    Obtient les informations du groupe en fonction des filtres spécifiés.

    Args:
    - filters (dict): Les filtres pour la comparaison.
    - application_train_test (pd.DataFrame): Le DataFrame contenant les données du groupe.

    Returns:
    - pd.DataFrame: Les informations filtrées du groupe pour la comparaison.
    """
    filtered_data = application_train_test[
        ['SK_ID_CURR',
         'TARGET',
         'DAYS_BIRTH',
         'CODE_GENDER',
         'OCCUPATION_TYPE',
         'AMT_CREDIT',
         'AMT_ANNUITY',
         'AMT_INCOME_TOTAL',
         'AMT_GOODS_PRICE',
         'DAYS_EMPLOYED',
         'CNT_FAM_MEMBERS',
         'EXT_SOURCE_1',
         'EXT_SOURCE_2',
         'EXT_SOURCE_3',
         ]]
    del application_train_test
    if 'age_group' in filters:
        filtered_data['AGE_GROUP'] = filtered_data['DAYS_BIRTH'].apply(determine_age_group)
        filtered_data = filtered_data[filtered_data['AGE_GROUP'] == filters['age_group']]
    if 'sex_filter' in filters:
        filtered_data = filtered_data[filtered_data['CODE_GENDER'] == filters['sex']]
    if 'job_filter' in filters:
        filtered_data = filtered_data[filtered_data['OCCUPATION_TYPE'] == filters['job']]
    return filtered_data


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

def get_column_name(indicator):
    """
    Obtient le nom de la colonne correspondant à un indicateur.

    Args:
    - indicator (str): L'indicateur dont on veut obtenir le nom de la colonne.

    Returns:
    - str: Le nom de la colonne correspondant à l'indicateur.
           Retourne None si l'indicateur n'est pas trouvé.
    """
    for key, value in correspondance_dict_application_info.items():
        if value['Titre'] == indicator:
            return key
    return None

st.title("Page de comparaison avec d'autres clients")
# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')
    st.session_state.client_id = None
    st.session_state.client_info = None
    st.session_state.client_features = None
    st.session_state.application_train_test = None
else :
    # Récupère l'ID client de la session state
    client_id = st.session_state.client_id
    client_info = st.session_state.client_info
    client_features = st.session_state.client_features
    application_info = client_info['informations_application'][0]
    application_train_test = st.session_state.application_train_test

    try:
        # Interface utilisateur Streamlit
        comparison_mode = st.selectbox(
            'Mode de comparaison:',
            ['Ensemble du groupe', 'Par groupe d\'âge', 'Par genre', 'Par type d\'emploi']
            )

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

        if comparison_mode == 'Par groupe d\'âge':
            st.write('Donnée associée du client:', filters['age_group'])
        elif comparison_mode == 'Par genre':
            st.write('Donnée associée du client:', filters['sex'])
        elif comparison_mode == 'Par type d\'emploi':
            st.write('Donnée associée du client:', filters['job'])

        # Obtention des informations du groupe depuis l'API Flask en utilisant les filtres
        group_info_for_comparison = get_group_info_for_comparison(filters, application_train_test)
        del application_train_test
        # Obtention des colonnes disponibles pour l'indicateur
        available_columns = [col for col in group_info_for_comparison.columns if col not in
                             ['SK_ID_CURR',
                              'DAYS_BIRTH',
                              'CODE_GENDER',
                              'OCCUPATION_TYPE',
                              'AGE_GROUP',]
                             ]

        # Obtention des titres correspondants aux clés du dictionnaire de correspondance
        indicator_titles = [
            correspondance_dict_application_info[col]['Titre'] for col in available_columns
            ]
        selected_indicator = st.selectbox('Indicateur de comparaison:', indicator_titles)
        selected_column = get_column_name(selected_indicator)
        # Calcul de la moyenne pour les clients
        average_group = group_info_for_comparison[selected_column].mean()
        target_client = application_info[selected_column]
        seuill = load_classification_threshold()

        # Graphique : Comparaison
        fig = go.Figure()
        # Ajout des barres avec la couleur grise
        fig.add_trace(go.Bar(
            x=['Client', 'Moyenne pour les individus'],
            y=[target_client, average_group],
            marker_color= 'gray',
            name=f'{selected_indicator} du client',
            text=[f'{value:.2f}' for value in [target_client, average_group]],
            textposition='auto',  # Positionner automatiquement le texte
        ))

        # Mise en forme du layout
        fig.update_layout(
            title=f'Comparaison des {selected_indicator} du client et des individus de comparaison',
            yaxis_title=f'Moyenne des {selected_indicator}',
            xaxis_title='Groupe',
            barmode='relative',
        )
        # Ajuste la taille du graphique
        fig.update_layout(height=600)

        # Affiche le graphique dans Streamlit
        st.plotly_chart(fig)

    except Exception as e:
        st.json({'error': str(e), 'status_code': 500})
