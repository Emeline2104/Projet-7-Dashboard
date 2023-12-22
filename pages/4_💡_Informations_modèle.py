"""
Script 4_💡_Informations_modèle.py

Ce script Streamlit affiche les informations sur l'importance globale des caractéristiques 
du modèle d'apprentissage automatique utilisé pour évaluer le risque de défaut de crédit. 
Il présente un graphique des 20 caractéristiques les plus importantes.

Prérequis :
- Streamlit doit être installé : pip install streamlit
- Requests doit être installé : pip install requests
- Plotly doit être installé : pip install plotly
- Pandas doit être installé : pip install pandas
"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# Environnement local
# api_url = "http://127.0.0.1:5001"
# Environnement Heroku
api_url = "https://projet-7-38cdf763d118.herokuapp.com/"

st.title("Page d'information sur le modèle")

def get_global_feature_importance():
    st.write(
        "Un modèle d'apprentissage automatique a été utilisé pour évaluer l'importance des différentes informations clients dans la prédiction du risque de défaut de crédit."
        )
    # Appel de l'API pour obtenir l'importance globale des caractéristiques
    st.header("Caractéristiques principales du modèle:")
    response = requests.get(f"{api_url}/get_global_feature_importance")

    if response.status_code == 200:
        # Convertis la réponse JSON en DataFrame
        importance_df = pd.DataFrame(response.json())

        # Sélectionne les 20 caractéristiques les plus importantes
        top_features = importance_df.head(20)
        top_features = top_features[['Feature', 'Coefficient']]
        # Créee le graphique à barres avec Plotly
        fig = go.Figure()

        # Ajoute les barres avec la couleur grise
        fig.add_trace(go.Bar(
            x=top_features['Feature'],
            y=top_features['Coefficient'],
            marker_color='#808080',  # Couleur grise
        ))

        # Mise en forme du layout
        fig.update_layout(
            title='Top 20 des caractéristiques les plus importantes: ',
            yaxis_title='Coefficient',
            xaxis_title='Caractéristiques',
            barmode='relative',
        )

        # Ajuste la taille du graphique
        fig.update_layout(height=800)

        # Streamlit app
        st.plotly_chart(fig)

        st.markdown(
            """
            Le graphique affiche les 20 facteurs les plus influents pour le modèle.
            Voici quelques points clés à retenir sur les informations ayant le plus d'importance pour la décision d'octroi du crédit :
            - **Sources externes de notation** (EXT_SOURCE_1, EXT_SOURCE_2, EXT_SOURCE_3) : Ces scores, provenant de sources externes, sont des indicateurs cruciaux pour évaluer la fiabilité financière des clients.
            - **Taux de paiement** (PAYMENT_RATE) : La façon dont les paiements sont effectués est un facteur déterminant. Un taux de paiement élevé est associé à une meilleure capacité de remboursement.
            - **Âge du client** (DAYS_BIRTH) : L'âge du client joue un rôle crucial. Des clients plus jeunes peuvent être considérés comme plus risqués.
            - **Mensualité du prêt** (AMT_ANNUITY) : La mensualité du prêt est importante. Des mensualités plus élevées par rapport au revenu peuvent indiquer un risque plus élevé.
            - **Ancienneté de l'emploi** (DAYS_EMPLOYED) : Plus le client est longtemps employé, plus il est stable financièrement.
            - **Proportion annuité/revenu** (ANNUITY_INCOME_PERC) : Cette proportion peut indiquer le niveau de confort financier du client.
            - **Délai depuis le dernier changement d'identité** (DAYS_ID_PUBLISH) : Des changements fréquents peuvent être associés à un risque plus élevé.
            - **Proportion de jours employés par rapport à l'âge** (DAYS_EMPLOYED_PERC) : Mesure la stabilité de l'emploi tout au long de la vie.
            - **Nombre moyen de paiements approuvés** (APPROVED_CNT_PAYMENT_MEAN) : Un indicateur de la gestion des paiements approuvés.
            - **Nombre maximal de jours de crédit actifs** (ACTIVE_DAYS_CREDIT_MAX) : Un historique de crédit actif plus long peut indiquer une stabilité financière.
            - **Délai depuis la dernière inscription** (DAYS_REGISTRATION) / **Délai minimal de crédit actif** (ACTIVE_DAYS_CREDIT_ENDDATE_MIN) / **Moyenne des retards de paiement** (INSTAL_DPD_MEAN) : Ces facteurs contribuent à évaluer la stabilité financière et la gestion du crédit.
            - **Montant du crédit** (AMT_CREDIT) / **Prix des biens** (AMT_GOODS_PRICE) / **Montant total des paiements d'acompte** (INSTAL_AMT_PAYMENT_SUM) : Des indicateurs importants pour évaluer la capacité du client à gérer les montants financiers associés au crédit.
            - **Nombre maximal de jours d'entrée de paiement** (INSTAL_DAYS_ENTRY_PAYMENT_MAX) / Nombre moyen de paiements précédents (**PREV_CNT_PAYMENT_MEAN**) : Des indicateurs liés aux paiements précédents.
            
            Ces facteurs permette de mieux comprendre comment le modèle prend ses décisions. 📊✨
            """)
    else:
        st.error(f"Erreur lors de la récupération de l'importance globale des caractéristiques : {response.status_code}")

get_global_feature_importance()
