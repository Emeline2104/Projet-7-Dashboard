# 1_📊_Informations_client.py
import streamlit as st
import requests

# Environnement local
#api_url = "http://127.0.0.1:5001"
# Environnement Heroku
api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

# Check que la clé 'client_id' est dans la session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = None

# Récupération de l'ID client de la session state
client_id = st.session_state.client_id


# a bouger
correspondance_dict_application_info = {
    'SK_ID_CURR': {'Titre': 'ID du prêt dans notre échantillon', 'Unité': ''},
    'TARGET': {'Titre': 'Variable cible', "Description": "1 - Client en difficulté de paiement : retard de paiement de plus de X jours sur au moins l'une des Y premières échéances du prêt dans notre échantillon, 0 - tous les autres cas", 'Unité': ''},
    'NAME_CONTRACT_TYPE': {'Titre': 'Type de contrat de prêt', 'Unité': ''},
    'CODE_GENDER': {'Titre': 'Genre du client', 'Unité': ''},
    'FLAG_OWN_CAR': {'Titre': "Possession d'une voiture", 'Unité': ''},
    'FLAG_OWN_REALTY': {'Titre': "Possession d'un bien immobilier", 'Unité': ''},
    'CNT_CHILDREN': {'Titre': "Nombre d'enfants", 'Unité': ''},
    'AMT_INCOME_TOTAL': {'Titre': 'Revenu total', 'Unité': 'Monnaie'},
    'AMT_CREDIT': {'Titre': 'Montant du crédit', 'Unité': 'Monnaie'},
    'AMT_ANNUITY': {'Titre': 'Annuité du prêt', 'Unité': 'Monnaie'},
    'AMT_GOODS_PRICE': {'Titre': 'Prix des biens', 'Description': 'Pour les prêts à la consommation, c\'est le prix des biens pour lesquels le prêt est accordé', 'Unité': 'Monnaie'},
    'NAME_TYPE_SUITE': {'Titre': 'Personne accompagnant le client lors de la demande de prêt', 'Unité': ''},
    'NAME_INCOME_TYPE': {'Titre': 'Type de revenu du client', 'Unité': ''},
    'NAME_EDUCATION_TYPE': {'Titre': "Niveau d'éducation le plus élevé atteint par le client", 'Unité': ''},
    'NAME_FAMILY_STATUS': {'Titre': 'Statut familial du client', 'Unité': ''},
    'NAME_HOUSING_TYPE': {'Titre': 'Situation de logement du client', 'Unité': ''},
    'REGION_POPULATION_RELATIVE': {'Titre': 'Population normalisée de la région où vit le client', 'Unité': ''},
    'DAYS_BIRTH': {'Titre': 'Âge du client en jours au moment de la demande', 'Unité': 'Jours'},
    'DAYS_EMPLOYED': {'Titre': 'Nombre de jours avant la demande où la personne a commencé son emploi actuel', 'Unité': 'Jours'},
    'DAYS_REGISTRATION': {'Titre': 'Nombre de jours avant la demande où le client a changé son enregistrement', 'Unité': 'Jours'},
    'DAYS_ID_PUBLISH': {'Titre': "Nombre de jours avant la demande où le client a changé le document d'identité avec lequel il a fait la demande de prêt", 'Unité': 'Jours'},
    'OWN_CAR_AGE': {'Titre': "Âge de la voiture du client", 'Unité': 'Années'},
    'FLAG_MOBIL': {'Titre': 'Le client a-t-il fourni un téléphone portable', 'Unité': ''},
    'FLAG_EMP_PHONE': {'Titre': 'Le client a-t-il fourni un téléphone professionnel', 'Unité': ''},
    'FLAG_WORK_PHONE': {'Titre': 'Le client a-t-il fourni un téléphone domicile', 'Unité': ''},
    'FLAG_CONT_MOBILE': {'Titre': 'Le téléphone portable était-il joignable', 'Unité': ''},
    'FLAG_PHONE': {'Titre': 'Le client a-t-il fourni un téléphone domicile', 'Unité': ''},
    'FLAG_EMAIL': {'Titre': 'Le client a-t-il fourni une adresse e-mail', 'Unité': ''},
    'OCCUPATION_TYPE': {'Titre': "Type d'occupation du client", 'Unité': ''},
    'CNT_FAM_MEMBERS': {'Titre': 'Nombre de membres de la famille', 'Unité': ''},
    'REGION_RATING_CLIENT': {'Titre': 'Notre évaluation de la région où vit le client', 'Unité': ''},
    'REGION_RATING_CLIENT_W_CITY': {'Titre': "Notre évaluation de la région où vit le client en tenant compte de la ville", 'Unité': ''},
    'WEEKDAY_APPR_PROCESS_START': {'Titre': 'Jour de la semaine où le client a fait la demande de prêt', 'Unité': ''},
    'HOUR_APPR_PROCESS_START': {'Titre': 'À quelle heure approximativement le client a-t-il fait la demande de prêt', 'Unité': 'Heures'},
    'REG_REGION_NOT_LIVE_REGION': {'Titre': "Drapeau si l'adresse permanente du client ne correspond pas à l'adresse de contact (1 = différent, 0 = même, au niveau régional)", 'Unité': ''},
    'REG_REGION_NOT_WORK_REGION': {'Titre': "Drapeau si l'adresse permanente du client ne correspond pas à l'adresse professionnelle (1 = différent, 0 = même, au niveau régional)", 'Unité': ''},
    'LIVE_REGION_NOT_WORK_REGION': {'Titre': "Drapeau si l'adresse de contact du client ne correspond pas à l'adresse professionnelle (1 = différent, 0 = même, au niveau régional)", 'Unité': ''},
    'REG_CITY_NOT_LIVE_CITY': {'Titre': "Drapeau si l'adresse permanente du client ne correspond pas à l'adresse de contact (1 = différent, 0 = même, au niveau de la ville)", 'Unité': ''},
    'REG_CITY_NOT_WORK_CITY': {'Titre': "Drapeau si l'adresse permanente du client ne correspond pas à l'adresse professionnelle (1 = différent, 0 = même, au niveau de la ville)", 'Unité': ''},
    'LIVE_CITY_NOT_WORK_CITY': {'Titre': "Drapeau si l'adresse de contact du client ne correspond pas à l'adresse professionnelle (1 = différent, 0 = même, au niveau de la ville)", 'Unité': ''},
    'ORGANIZATION_TYPE': {'Titre': "Type d'organisation où le client travaille", 'Unité': ''},
    'EXT_SOURCE_1': {'Titre': 'Score normalisé à partir de la source de données externe 1', 'Unité': ''},
    'EXT_SOURCE_2': {'Titre': 'Score normalisé à partir de la source de données externe 2', 'Unité': ''},
    'EXT_SOURCE_3': {'Titre': 'Score normalisé à partir de la source de données externe 3', 'Unité': ''},
    'APARTMENTS_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille moyenne de l\'appartement', 'Unité': ''},
    'BASEMENTAREA_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Surface moyenne du sous-sol', 'Unité': ''},
    'YEARS_BEGINEXPLUATATION_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Âge moyen du début de l\'exploitation', 'Unité': ''},
    'YEARS_BUILD_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Âge moyen du bâtiment', 'Unité': ''},
    'COMMONAREA_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille moyenne de la zone commune', 'Unité': ''},
    'ELEVATORS_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre moyen d\'ascenseurs', 'Unité': ''},
    'ENTRANCES_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre moyen d\'entrées', 'Unité': ''},
    'FLOORSMAX_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre moyen d\'étages maximum', 'Unité': ''},
    'FLOORSMIN_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre moyen d\'étages minimum', 'Unité': ''},
    'LANDAREA_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Surface moyenne du terrain', 'Unité': ''},
    'LIVINGAPARTMENTS_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille moyenne des appartements', 'Unité': ''},
    'LIVINGAREA_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille moyenne de la surface habitable', 'Unité': ''},
    'NONLIVINGAPARTMENTS_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre moyen d\'appartements non habitables', 'Unité': ''},
    'NONLIVINGAREA_AVG': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille moyenne de la zone non habitable', 'Unité': ''},
    'APARTMENTS_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille modale de l\'appartement', 'Unité': ''},
    'BASEMENTAREA_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Surface modale du sous-sol', 'Unité': ''},
    'YEARS_BEGINEXPLUATATION_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Âge modal du début de l\'exploitation', 'Unité': ''},
    'YEARS_BUILD_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Âge modal du bâtiment', 'Unité': ''},
    'COMMONAREA_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille modale de la zone commune', 'Unité': ''},
    'ELEVATORS_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre modal d\'ascenseurs', 'Unité': ''},
    'ENTRANCES_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre modal d\'entrées', 'Unité': ''},
    'FLOORSMAX_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre modal d\'étages maximum', 'Unité': ''},
    'FLOORSMIN_MEDI': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille médiane de l\'appartement', 'Unité': 'normalized'},
    'LANDAREA_MEDI': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Surface médiane du terrain', 'Unité': 'normalized'},
    'LIVINGAPARTMENTS_MEDI': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille médiane des appartements', 'Unité': 'normalized'},
    'LIVINGAREA_MEDI': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille médiane de la surface habitable', 'Unité': 'normalized'},
    'NONLIVINGAPARTMENTS_MEDI': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Nombre médian d\'appartements non habitables', 'Unité': 'normalized'},
    'NONLIVINGAREA_MEDI': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Taille médiane de la zone non habitable', 'Unité': 'normalized'},
    'FONDKAPREMONT_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Mode de fonds de rénovation', 'Unité': 'normalized'},
    'HOUSETYPE_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Mode de type de maison', 'Unité': 'normalized'},
    'TOTALAREA_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Mode de surface totale', 'Unité': 'normalized'},
    'WALLSMATERIAL_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Mode de matériau des murs', 'Unité': 'normalized'},
    'EMERGENCYSTATE_MODE': {'Titre': 'Informations normalisées sur le bâtiment où vit le client', 'Description': 'Mode d\'état d\'urgence', 'Unité': 'normalized'},
    'OBS_30_CNT_SOCIAL_CIRCLE': {'Titre': 'Nombre d\'observations du cercle social du client avec un retard de paiement de 30 jours', 'Unité': ''},
    'DEF_30_CNT_SOCIAL_CIRCLE': {'Titre': 'Nombre d\'observations du cercle social du client avec défaut de paiement de 30 jours', 'Unité': ''},
    'OBS_60_CNT_SOCIAL_CIRCLE': {'Titre': 'Nombre d\'observations du cercle social du client avec un retard de paiement de 60 jours', 'Unité': ''},
    'DEF_60_CNT_SOCIAL_CIRCLE': {'Titre': 'Nombre d\'observations du cercle social du client avec défaut de paiement de 60 jours', 'Unité': ''},
    'DAYS_LAST_PHONE_CHANGE': {'Titre': 'Nombre de jours avant la demande où le client a changé de téléphone', 'Unité': 'Jours'},
    'FLAG_DOCUMENT_2': {'Titre': 'Le client a-t-il fourni le document 2', 'Unité': ''},
    'FLAG_DOCUMENT_3': {'Titre': 'Le client a-t-il fourni le document 3', 'Unité': ''},
    'FLAG_DOCUMENT_4': {'Titre': 'Le client a-t-il fourni le document 4', 'Unité': ''},
    'FLAG_DOCUMENT_5': {'Titre': 'Le client a-t-il fourni le document 5', 'Unité': ''},
    'FLAG_DOCUMENT_6': {'Titre': 'Le client a-t-il fourni le document 6', 'Unité': ''},
    'FLAG_DOCUMENT_7': {'Titre': 'Le client a-t-il fourni le document 7', 'Unité': ''},
    'FLAG_DOCUMENT_8': {'Titre': 'Le client a-t-il fourni le document 8', 'Unité': ''},
    'FLAG_DOCUMENT_9': {'Titre': 'Le client a-t-il fourni le document 9', 'Unité': ''},
    'FLAG_DOCUMENT_10': {'Titre': 'Le client a-t-il fourni le document 10', 'Unité': ''},
    'FLAG_DOCUMENT_11': {'Titre': 'Le client a-t-il fourni le document 11', 'Unité': ''},
    'FLAG_DOCUMENT_12': {'Titre': 'Le client a-t-il fourni le document 12', 'Unité': ''},
    'FLAG_DOCUMENT_13': {'Titre': 'Le client a-t-il fourni le document 13', 'Unité': ''},
    'FLAG_DOCUMENT_14': {'Titre': 'Le client a-t-il fourni le document 14', 'Unité': ''},
    'FLAG_DOCUMENT_15': {'Titre': 'Le client a-t-il fourni le document 15', 'Unité': ''},
    'FLAG_DOCUMENT_16': {'Titre': 'Le client a-t-il fourni le document 16', 'Unité': ''},
    'FLAG_DOCUMENT_17': {'Titre': 'Le client a-t-il fourni le document 17', 'Unité': ''},
    'FLAG_DOCUMENT_18': {'Titre': 'Le client a-t-il fourni le document 18', 'Unité': ''},
    'FLAG_DOCUMENT_19': {'Titre': 'Le client a-t-il fourni le document 19', 'Unité': ''},
    'FLAG_DOCUMENT_20': {'Titre': 'Le client a-t-il fourni le document 20', 'Unité': ''},
    'FLAG_DOCUMENT_21': {'Titre': 'Le client a-t-il fourni le document 21', 'Unité': ''},
    'AMT_REQ_CREDIT_BUREAU_HOUR': {'Titre': 'Nombre de demandes au bureau de crédit une heure avant la demande du client', 'Unité': ''},
    'AMT_REQ_CREDIT_BUREAU_DAY': {'Titre': 'Nombre de demandes au bureau de crédit un jour avant la demande du client (à l\'exclusion d\'une heure avant la demande)', 'Unité': ''},
    'AMT_REQ_CREDIT_BUREAU_WEEK': {'Titre': 'Nombre de demandes au bureau de crédit une semaine avant la demande du client (à l\'exclusion d\'un jour avant la demande)', 'Unité': ''},
    'AMT_REQ_CREDIT_BUREAU_MON': {'Titre': 'Nombre de demandes au bureau de crédit un mois avant la demande du client (à l\'exclusion d\'une semaine avant la demande)', 'Unité': ''},
    'AMT_REQ_CREDIT_BUREAU_QRT': {'Titre': 'Nombre de demandes au bureau de crédit trois mois avant la demande du client (à l\'exclusion d\'un mois avant la demande)', 'Unité': ''},
    'AMT_REQ_CREDIT_BUREAU_YEAR': {'Titre': 'Nombre de demandes au bureau de crédit un an avant la demande du client (à l\'exclusion des trois derniers mois avant la demande)', 'Unité': ''}
}

correspondance_dict_bureau_info = {
    'SK_ID_CURR': {'Titre': 'ID Prêt', 'Description': 'ID du prêt dans notre échantillon', 'Unité': ''},
    'SK_BUREAU_ID': {'Titre': 'ID Crédit Recodé', 'Description': 'ID recodé du crédit précédent du Bureau de crédit', 'Unité': ''},
    'CREDIT_ACTIVE': {'Titre': 'Statut Crédit', 'Description': 'Statut des crédits signalés par le Bureau de crédit', 'Unité': ''},
    'CREDIT_CURRENCY': {'Titre': 'Devise Crédit', 'Description': 'Devise recodée du crédit du Bureau de crédit', 'Unité': ''},
    'DAYS_CREDIT': {'Titre': 'Jours Avant Crédit', 'Description': 'Jours avant la demande actuelle où le client a demandé un crédit au Bureau de crédit', 'Unité': 'Jours'},
    'CREDIT_DAY_OVERDUE': {'Titre': 'Jours Retard Crédit', 'Description': 'Nombre de jours de retard sur le crédit du Bureau de crédit au moment de la demande', 'Unité': 'Jours'},
    'DAYS_CREDIT_ENDDATE': {'Titre': 'Durée Restante Crédit', 'Description': 'Durée restante du crédit du Bureau de crédit au moment de la demande chez Home Credit', 'Unité': 'Jours'},
    'DAYS_ENDDATE_FACT': {'Titre': 'Jours Depuis Fin Crédit', 'Description': 'Jours depuis la fin du crédit du Bureau de crédit au moment de la demande chez Home Credit', 'Unité': 'Jours'},
    'AMT_CREDIT_MAX_OVERDUE': {'Titre': 'Max Retard Crédit', 'Description': "Montant maximal de retard sur le crédit du Bureau de crédit jusqu'à présent", 'Unité': 'Monnaie'},
    'CNT_CREDIT_PROLONG': {'Titre': 'Nombre Prolongations', 'Description': 'Nombre de fois où le crédit du Bureau de crédit a été prolongé', 'Unité': ''},
    'AMT_CREDIT_SUM': {'Titre': 'Montant Crédit Actuel', 'Description': 'Montant de crédit actuel pour le crédit du Bureau de crédit', 'Unité': 'Monnaie'},
    'AMT_CREDIT_SUM_DEBT': {'Titre': 'Dette Actuelle', 'Description': 'Dette actuelle sur le crédit du Bureau de crédit', 'Unité': 'Monnaie'},
    'AMT_CREDIT_SUM_LIMIT': {'Titre': 'Limite Crédit Actuelle', 'Description': 'Limite de crédit actuelle de la carte de crédit signalée au Bureau de crédit', 'Unité': 'Monnaie'},
    'AMT_CREDIT_SUM_OVERDUE': {'Titre': 'Montant Actuel en Souffrance', 'Description': 'Montant actuel en souffrance sur le crédit du Bureau de crédit', 'Unité': 'Monnaie'},
    'CREDIT_TYPE': {'Titre': 'Type Crédit', 'Description': 'Type de crédit du Bureau de crédit', 'Unité': ''},
    'DAYS_CREDIT_UPDATE': {'Titre': 'Jours Avant Mise à Jour', 'Description': 'Jours avant la demande de prêt où la dernière information sur le crédit du Bureau de crédit a été mise à jour', 'Unité': 'Jours'},
    'AMT_ANNUITY': {'Titre': 'Annuité Crédit', 'Description': 'Annuité du crédit du Bureau de crédit', 'Unité': 'Monnaie'},
}

correspondance_dict_bureau_balance_info = {
    'SK_BUREAU_ID': {'Titre': 'ID Crédit Recodé', 'Description': 'ID recodé du crédit du Bureau de crédit', 'Unité': ''},
    'MONTHS_BALANCE': {'Titre': 'Mois Solde', 'Description': 'Mois de solde par rapport à la date de demande', 'Unité': ''},
    'STATUS': {'Titre': 'Statut Prêt', 'Description': 'Statut du prêt du Bureau de crédit pendant le mois', 'Unité': ''},
}

correspondance_dict_previous_application_info = {
    'SK_ID_PREV': {'Titre': 'ID Crédit Précédent', 'Description': 'Identifiant du crédit précédent chez Home Credit', 'Unité': ''},
    'SK_ID_CURR': {'Titre': 'ID Prêt', 'Description': 'Identifiant du prêt dans notre échantillon', 'Unité': ''},
    'NAME_CONTRACT_TYPE': {'Titre': 'Type de Contrat', 'Description': 'Type de contrat de la demande précédente (prêt en espèces, prêt à la consommation [POS],...)', 'Unité': ''},
    'AMT_ANNUITY': {'Titre': 'Annuité', 'Description': "Montant de l'annuité de la demande précédente", 'Unité': 'Monnaie'},
    'AMT_APPLICATION': {'Titre': 'Montant Demandé', 'Description': 'Montant demandé lors de la demande précédente', 'Unité': 'Monnaie'},
    'AMT_CREDIT': {'Titre': 'Montant du Crédit', 'Description': 'Montant final du crédit accordé lors de la demande précédente', 'Unité': 'Monnaie'},
    'AMT_DOWN_PAYMENT': {'Titre': 'Acompte', 'Description': "Montant de l'acompte lors de la demande précédente", 'Unité': 'Monnaie'},
    'AMT_GOODS_PRICE': {'Titre': 'Prix des Biens', 'Description': 'Prix des biens demandés lors de la demande précédente (si applicable)', 'Unité': 'Monnaie'},
    'WEEKDAY_APPR_PROCESS_START': {'Titre': 'Jour de Début du Traitement', 'Description': 'Jour de la semaine où le client a fait la demande précédente', 'Unité': ''},
    'HOUR_APPR_PROCESS_START': {'Titre': 'Heure de Début du Traitement', 'Description': 'Heure approximative où le client a fait la demande précédente', 'Unité': ''},
    'FLAG_LAST_APPL_PER_CONTRACT': {'Titre': 'Dernière Demande par Contrat', 'Description': "Drapeau indiquant si c'était la dernière demande pour le contrat précédent", 'Unité': ''},
    'NFLAG_LAST_APPL_IN_DAY': {'Titre': 'Dernière Demande du Jour', 'Description': 'Drapeau indiquant si la demande était la dernière de la journée pour le client', 'Unité': ''},
    'NFLAG_MICRO_CASH': {'Titre': 'Micro Finance Loan', 'Description': 'Drapeau indiquant un prêt de microfinance', 'Unité': ''},
    'RATE_DOWN_PAYMENT': {'Titre': 'Taux d\'Acompte', 'Description': 'Taux d\'acompte normalisé sur le crédit précédent', 'Unité': ''},
    'RATE_INTEREST_PRIMARY': {'Titre': 'Taux d\'Intérêt Primaire', 'Description': 'Taux d\'intérêt normalisé sur le crédit précédent', 'Unité': ''},
    'RATE_INTEREST_PRIVILEGED': {'Titre': 'Taux d\'Intérêt Privilégié', 'Description': 'Taux d\'intérêt normalisé privilégié sur le crédit précédent', 'Unité': ''},
    'NAME_CASH_LOAN_PURPOSE': {'Titre': 'Objet du Prêt en Espèces', 'Description': 'Objectif du prêt en espèces lors de la demande précédente', 'Unité': ''},
    'NAME_CONTRACT_STATUS': {'Titre': 'Statut du Contrat', 'Description': 'Statut du contrat de la demande précédente (approuvé, annulé, ...)', 'Unité': ''},
    'DAYS_DECISION': {'Titre': "Jours jusqu'à Décision", 'Description': "Nombre de jours avant la décision par rapport à la demande actuelle", 'Unité': 'Jours'},
    'NAME_PAYMENT_TYPE': {'Titre': 'Méthode de Paiement', 'Description': 'Méthode de paiement choisie par le client pour la demande précédente', 'Unité': ''},
    'CODE_REJECT_REASON': {'Titre': 'Raison du Rejet', 'Description': 'Raison du rejet de la demande précédente', 'Unité': ''},
    'NAME_TYPE_SUITE': {'Titre': 'Accompagnant lors de la Demande', 'Description': 'Personne accompagnant le client lors de la demande précédente', 'Unité': ''},
    'NAME_CLIENT_TYPE': {'Titre': 'Type de Client', 'Description': 'Ancien ou nouveau client lors de la demande précédente', 'Unité': ''},
    'NAME_GOODS_CATEGORY': {'Titre': 'Catégorie des Biens', 'Description': 'Type de biens pour lesquels le client a demandé dans la demande précédente', 'Unité': ''},
    'NAME_PORTFOLIO': {'Titre': 'Portefeuille', 'Description': 'Type de portefeuille pour la demande précédente (CASH, POS, CAR, …)', 'Unité': ''},
    'NAME_PRODUCT_TYPE': {'Titre': 'Type de Produit', 'Description': 'Type de produit pour la demande précédente (x-sell ou walk-in)', 'Unité': ''},
    'CHANNEL_TYPE': {'Titre': 'Type de Canal', 'Description': 'Canal par lequel le client a été acquis lors de la demande précédente', 'Unité': ''},
    'SELLERPLACE_AREA': {'Titre': 'Zone de Vente du Vendeur', 'Description': 'Zone de vente du lieu du vendeur pour la demande précédente', 'Unité': ''},
    'NAME_SELLER_INDUSTRY': {'Titre': 'Industrie du Vendeur', 'Description': 'Industrie du vendeur pour la demande précédente', 'Unité': ''},
    'CNT_PAYMENT': {'Titre': 'Nombre de Paiements', 'Description': 'Terme du crédit précédent au moment de la demande précédente', 'Unité': ''},
    'NAME_YIELD_GROUP': {'Titre': 'Groupe de Rendement', 'Description': "Taux d'intérêt regroupé en petits, moyens et grands du crédit précédent", 'Unité': ''},
    'PRODUCT_COMBINATION': {'Titre': 'Combinaison de Produits', 'Description': 'Combinaison détaillée des produits pour la demande précédente', 'Unité': ''},
    'DAYS_FIRST_DRAWING': {'Titre': "Jours jusqu'à la Première Libération", 'Description': 'Nombre de jours avant la première libération par rapport à la demande actuelle', 'Unité': 'Jours'},
    'DAYS_FIRST_DUE': {'Titre': "Jours jusqu'à la Première Échéance", 'Description': 'Nombre de jours avant la première échéance prévue par rapport à la demande actuelle', 'Unité': 'Jours'},
    'DAYS_LAST_DUE_1ST_VERSION': {'Titre': "Jours jusqu'à la Première Échéance (Version 1)", 'Description': 'Nombre de jours avant la première échéance par rapport à la demande actuelle (première version)', 'Unité': 'Jours'},
    'DAYS_LAST_DUE': {'Titre': "Jours jusqu'à la Dernière Échéance', 'Description': 'Nombre de jours avant la dernière échéance par rapport à la demande actuelle", 'Unité': 'Jours'},
    'DAYS_TERMINATION': {'Titre': "Jours jusqu'à la Résiliation Attendue", 'Description': 'Nombre de jours avant la résiliation attendue par rapport à la demande actuelle', 'Unité': 'Jours'},
    'NFLAG_INSURED_ON_APPROVAL': {'Titre': 'Assurance Demandée', 'Description': 'Drapeau indiquant si le client a demandé une assurance pendant la demande précédente', 'Unité': ''}
}


# Fonction pour afficher les informations sur le client
def afficher_informations_client(client_id):
    st.title("Page d'informations sur le client")
    st.subheader("Informations personnelles:")

    st.write(f"**ID du client :** {client_id}")

    try:
        # Affiche les informations sur le client
        response = requests.get(f"{api_url}/informations_client_brut/{client_id}")
        client_info = response.json()
        # Affiche les informations les plus importantes sur l'application
        if 'application_info' in client_info:
            afficher_informations_application(client_info['application_info'][0])

        # Affiche les informations sur le bureau
        if 'bureau_info' in client_info:
            afficher_informations_bureau(client_info['bureau_info'][0])

        # Affiche les informations sur les demandes précédentes
        if 'previous_application_info' in client_info:
            afficher_informations_previous_application(client_info['previous_application_info'][0])

        # Affiche d'autres informations dans une liste déroulante
        # afficher_informations_supplementaires(client_info)

    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

# Fonction pour afficher les informations les plus importantes sur l'application
def afficher_informations_application(application_info):
    st.subheader("Informations générales:")

    # Liste des titres associés aux clés du dictionnaire
    titres_informations = [correspondance_dict_application_info[key]['Titre'] for key in correspondance_dict_application_info.keys()]

    # Liste déroulante pour choisir l'information
    choix_information = st.selectbox("Choisir une information:", titres_informations)

    # Trouver la clé correspondante dans application_info
    for key, value in correspondance_dict_application_info.items():
        if value['Titre'] == choix_information:
            cle_correspondante = key
            break

    # Afficher les données correspondantes
    st.write(f"Valeur : {application_info[cle_correspondante]}")
    st.write(f"Unité : {value.get('Unité', 'Aucune unité disponible')}")
    st.write(f"Description : {value.get('Description', 'Aucune description disponible')}")

# Fonction pour afficher les informations sur le bureau
def afficher_informations_bureau(bureau_info):
    st.subheader("Informations concernant les données des institutions financières:")

    # Liste des titres associés aux clés du dictionnaire
    titres_informations = [correspondance_dict_bureau_info[key]['Titre'] for key in correspondance_dict_bureau_info.keys()]

    # Liste déroulante pour choisir l'information
    choix_information = st.selectbox("Choisir une information:", titres_informations)

    # Trouver la clé correspondante dans application_info
    for key, value in correspondance_dict_bureau_info.items():
        if value['Titre'] == choix_information:
            cle_correspondante = key
            break

    # Afficher les données correspondantes
    st.write(f"Valeur : {bureau_info[cle_correspondante]}")
    st.write(f"Unité : {value.get('Unité', 'Aucune unité disponible')}")
    st.write(f"Description : {value.get('Description', 'Aucune description disponible')}")


# Fonction pour afficher les informations sur les demandes précédentes
def afficher_informations_previous_application(previous_application_info):
    st.subheader("Informations sur les anciennes demandes:")
    # Liste des titres associés aux clés du dictionnaire
    titres_informations = [correspondance_dict_previous_application_info[key]['Titre'] for key in correspondance_dict_previous_application_info.keys()]

    # Liste déroulante pour choisir l'information
    choix_information = st.selectbox("Choisir une information:", titres_informations)

    # Trouver la clé correspondante dans application_info
    for key, value in correspondance_dict_previous_application_info.items():
        if value['Titre'] == choix_information:
            cle_correspondante = key
            break
        

    # Afficher les données correspondantes
    st.write(f"Information sélectionnée : {choix_information}")
    st.write(f"Valeur : {previous_application_info[cle_correspondante]}")
    st.write(f"Description : {value.get('Description', 'Aucune description disponible')}")
    st.write(f"Unité : {value.get('Unité', 'Aucune unité disponible')}")

# Fonction pour afficher les informations sur le POS_CASH_balance
def afficher_informations_pos_cash_balance(pos_cash_balance_info):
    st.subheader("POS_CASH_balance_info:")
    for entry in pos_cash_balance_info:
        st.write(entry)


# Fonction pour afficher les informations sur les paiements par carte de crédit
def afficher_informations_credit_card_balance(credit_card_balance_info):
    st.subheader("Credit Card Balance Info:")
    st.write(credit_card_balance_info)

# Fonction pour afficher les informations sur les paiements d'acomptes
def afficher_informations_installments_payments(installments_payments_info):
    st.subheader("Installments Payments Info:")
    for entry in installments_payments_info:
        st.write(entry)



# Fonction pour afficher des informations supplémentaires dans une liste déroulante
def afficher_informations_supplementaires(client_info):
    st.subheader("Informations supplémentaires:")
    with st.expander("Plus d'informations"):
        # Afficher les informations sur le POS_CASH_balance
        if 'POS_CASH_balance_info' in client_info:
            afficher_informations_pos_cash_balance(client_info['POS_CASH_balance_info'])

        # Afficher les informations sur le bureau
        if 'bureau_info' in client_info:
            afficher_informations_bureau(client_info['bureau_info'])

        # Afficher les informations sur les paiements par carte de crédit
        if 'credit_card_balance_info' in client_info:
            afficher_informations_credit_card_balance(client_info['credit_card_balance_info'])

        # Afficher les informations sur les paiements d'acomptes
        if 'installments_payments_info' in client_info:
            afficher_informations_installments_payments(client_info['installments_payments_info'])

# Si l'ID client est défini, affiche les informations sur le client
if client_id:
    afficher_informations_client(client_id)

else:
    st.write('Merci de vouloir indiquer un ID client dans "Recherche client".')

# To do -> mettre que les infos les plus importantes puis liste déroulante pour les autres ? 
# essayer d'afficher les informations précises avec des JSON
#         response = requests.get(f"{api_url}/predict/{client_id}")
# Finir d'afficher les informations bien + mettre les informations relatigves à la demande de prêt dans l'autre onglet 
# pret sur autre onglet et faire requete dans recherche ? puis enregistrer en variables globale 

