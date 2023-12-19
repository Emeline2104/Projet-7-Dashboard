import streamlit as st
import requests
import pandas as pd
import csv

def set_background_color():
    # Définit la couleur de fond de la page en utilisant du code HTML dans une balise style
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_home_page():
    # Affiche la page d'accueil avec le titre, l'image et les informations générales
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

def data_reader(file_path, chunk_size=2000000): # a sup 
    # Ouvre le fichier en utilisant l'itérateur de pandas
    data_reader = pd.read_csv(file_path, chunksize=chunk_size)
    
    # Itére à travers les morceaux
    for chunk in data_reader:
        # Renvoye chaque morceau
        yield chunk

@st.cache_data   
def data_reader(file_path):
    return pd.read_csv(file_path)


def obtenir_informations_brutes_client(client_id):
    # Initialise le dictionnaire pour stocker les informations
    informations_client = {}

    # Étape 1: Obtenez les informations de l'application (application_train et application_test)
    informations_application = obtenir_informations_par_table("Data/sampled/application_train_selected.csv", client_id)
    informations_client['informations_application'] = informations_application

    # Étape 2: Obtenez les informations du bureau
    informations_bureau = obtenir_informations_par_table("Data/sampled/bureau_selected.csv", client_id)
    informations_client['informations_bureau'] = informations_bureau

    # Étape 3: Obtenez les informations du bureau_balance en utilisant les informations du bureau
    #bureau_balance_info = obtenir_informations_bureau_balance(informations_bureau, data_reader)
    #informations_client['informations_bureau_balance'] = bureau_balance_info
    #del bureau_balance_info, informations_bureau

    # Étape 4: Obtenez les informations des applications précédentes
    informations_previous_application = obtenir_informations_par_table("Data/sampled/previous_application_selected.csv", client_id)
    informations_client['informations_previous_application'] = informations_previous_application

    # Étape 5: Obtenez les informations du POS_CASH_balance en utilisant les informations des applications précédentes
    #POS_CASH_balance_info = obtenir_informations_POS_CASH_balance(informations_previous_application, data_reader)
    #informations_client['informations_POS_CASH_balance'] = POS_CASH_balance_info
    #del POS_CASH_balance_info

    # Étape 6: Obtenez les informations des paiements d'installments en utilisant les informations des applications précédentes
    #installments_payments_info = obtenir_informations_installments_payments(informations_previous_application, data_reader)
    #informations_client['informations_installments_payments'] = installments_payments_info
    #del installments_payments_info, informations_previous_application

    # Étape 7: Obtenez les informations du credit_card_balance
    #informations_credit_card_balance = obtenir_informations_par_table("Data/sampled/credit_card_balance_selected.csv", client_id, data_reader)
    #informations_client['informations_credit_card_balance'] = informations_credit_card_balance
    #del informations_credit_card_balance

    return informations_client

def obtenir_informations_par_table(url, client_id):
    informations_table = pd.read_csv(url)
    informations_table = informations_table[informations_table['SK_ID_CURR'] == client_id]
    return informations_table.to_dict(orient='records')

def obtenir_informations_bureau_balance(informations_bureau, data_reader):
    bureau_balance_info = pd.DataFrame()
    bureau_balance_url = "Data/sampled/bureau_balance_selected.csv"
    informations_bureau = pd.DataFrame(informations_bureau)
    informations_bureau = informations_bureau.reset_index(drop=True)
    for morceau in data_reader(bureau_balance_url):
        if not informations_bureau.empty:
            morceau = morceau.reset_index(drop=True)
            morceau_info = morceau[morceau['SK_ID_BUREAU'].isin(informations_bureau['SK_ID_BUREAU'])]
        else:
            morceau_info = pd.DataFrame()
        bureau_balance_info = pd.concat([bureau_balance_info, morceau_info], ignore_index=True)
    return bureau_balance_info.to_dict(orient='records')

def obtenir_informations_POS_CASH_balance(informations_previous_application, data_reader):
    POS_CASH_balance_info = pd.DataFrame()
    POS_CASH_balance_url = "Data/sampled/POS_CASH_balance_selected.csv"
    informations_previous_application = pd.DataFrame(informations_previous_application)
    informations_previous_application = informations_previous_application.reset_index(drop=True)
    for morceau in data_reader(POS_CASH_balance_url):
        if not informations_previous_application.empty:
            morceau = morceau.reset_index(drop=True)
            morceau_info = morceau[morceau['SK_ID_PREV'].isin(informations_previous_application['SK_ID_PREV'])]
        else:
            morceau_info = pd.DataFrame()
        POS_CASH_balance_info = pd.concat([POS_CASH_balance_info, morceau_info], ignore_index=True)
    return POS_CASH_balance_info.to_dict(orient='records')

def obtenir_informations_installments_payments(informations_previous_application, data_reader):
    installments_payments_info = pd.DataFrame()
    installments_payments_url = "Data/sampled/installments_payments_selected.csv"
    informations_previous_application = pd.DataFrame(informations_previous_application)
    informations_previous_application = informations_previous_application.reset_index(drop=True)
    for morceau in data_reader(installments_payments_url):
        if not informations_previous_application.empty:
            morceau = morceau.reset_index(drop=True)
            morceau_info = morceau[morceau['SK_ID_PREV'].isin(informations_previous_application['SK_ID_PREV'])]
        else:
            morceau_info = pd.DataFrame()
        installments_payments_info = pd.concat([installments_payments_info, morceau_info], ignore_index=True)
    return installments_payments_info.to_dict(orient='records')

def replace_nan_with_none(d):
    for key, value in d.items():
        if pd.isna(value):
            d[key] = None
    return d

def get_client_features(client_id, data):
    client_id = int(client_id)
    client_features = data[data['SK_ID_CURR'] == client_id].to_dict(orient='records')

    if client_features:
        client_data = replace_nan_with_none(client_features[0])
        st.session_state.client_features = client_data
        return client_data
    else:
        return {'error': 'Client non trouvé'}

def obtenir_informations_client(client_id):
    # Utiliser la fonction de génération pour lire les données par morceaux
    lecteur_donnees = data_reader
    client_id = int(client_id)  # Convertir client_id en entier
    informations_client = obtenir_informations_brutes_client(client_id)
    return informations_client


def get_client_info_brut(client_id):
    client_info = obtenir_informations_client(client_id)
    st.session_state.client_info = client_info
    if client_info:
        return client_info
    else:
        return {'error': 'Client non trouvé'}

def main():
    set_background_color()
    show_home_page()

    client_id = st.text_input("ID du client:")
    st.session_state.client_id = client_id

    if st.button("Valider et accéder aux informations du client"):
        with st.spinner('Patientez un instant pour le chargement des données ...'):
            get_client_info_brut(client_id)
            data = data_reader("https://projet-7-aws.s3.eu-north-1.amazonaws.com/data_agregg.csv")
            application_train_test = data_reader("Data/sampled/application_train_selected.csv")
            st.session_state.application_train_test = application_train_test
            get_client_features(client_id, data)
        st.success('Vous pouvez accéder aux autres pages !')
    else:
        st.session_state.client_info = {}

if __name__ == "__main__":
    main()