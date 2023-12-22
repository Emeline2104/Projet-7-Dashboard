# Projet-7 - Prêt à Dépenser - Dashboard

Ce projet a été réalisé dans le cadre de la formation diplomante de Data Scientist d'OpenClassRooms & CentraleSupelec.

## A propos du projet : 
Ce projet "Prêt à Dépenser" vise à développer un modèle de scoring prédictif pour évaluer la probabilité de remboursement des clients dans le secteur financier. En parallèle, la création d'un dashboard interactif transparent permettra aux chargés de relation client d'interpréter les prédictions du modèle, répondant ainsi à la demande croissante des clients en matière de transparence dans le processus d'octroi de crédit.

### Objectifs : 
- Développer un modèle de scoring pour prédire la probabilité de remboursement des clients (*[repository du modèle et de l'API](https://github.com/Emeline2104/Projet-7-Models-API)*).
- Créer un dashboard interactif pour les chargés de relation client.
  
### Données : 
Les données nécessaires au projet sont disponibles [ici](https://www.kaggle.com/c/home-credit-default-risk/data).
Elles incluent des informations comportementales et financières.

### Livrables : 

#### Scripts : 
- Script principal du projet (*[Recherche_client.py](https://github.com/Emeline2104/Projet-7-Dashboard/blob/dashboard/Recherche_client.py)*) qui contient la logique de l'application Streamlit avec les pages suivantes :
  - Page 1 : Informations sur le client (*[1_📊_Informations_client.py](https://github.com/Emeline2104/Projet-7-Dashboard/blob/dashboard/pages/1_%F0%9F%93%8A_Informations_client.py)*);
  - Page 2 : Informations sur la demande de crédit (*[2_🚀 _Informations_crédit.py](https://github.com/Emeline2104/Projet-7-Dashboard/blob/dashboard/pages/2_%F0%9F%9A%80%20_Informations_cr%C3%A9dit.py)*);
  - Page 1 : Informations sur la comparaison entre le client et d'autres groupes (*[3_📈_Informations_comparaison.py](https://github.com/Emeline2104/Projet-7-Dashboard/blob/dashboard/pages/3_%F0%9F%93%88_Informations_comparaison.py))*);
  - Page 1 : Informations sur le modèle de scoring (*[4_💡_Informations_modèle.py](https://github.com/Emeline2104/Projet-7-Dashboard/blob/dashboard/pages/4_%F0%9F%92%A1_Informations_mod%C3%A8le.py)*);
- Script des tests unitaires nécessaires pour le déploiement automatique (*[test_dashboard.py](https://github.com/Emeline2104/Projet-7-Dashboard/blob/dashboard/tests/test_dashboard.py)*).
  
#### Fichier introductif du dahsboard 
Fichier introductif permettant de comprendre l'objectif du projet et le découpage des dossiers (*[]()*).
Fichier listant les packages utilisés seront présents dans les dossiers (*[]()*).


Exécution du script :
Pour exécuter le dashboard, assurez-vous d'avoir Python 3.11 ou supérieur installé et exécutez la commande suivante dans le terminal :

bash
Copy code
streamlit run src/dashboard.py
Assurez-vous également de personnaliser les chemins et les paramètres dans le fichier config.py selon les besoins de votre projet.

Structure du Projet
Le projet est organisé de la manière suivante :

.github/workflows:
tests.yml: Fichier de configuration pour les workflows GitHub.
src: Le répertoire principal du code source.
config.py: Fichier de configuration pour le projet.
dashboard.py: Script principal de l'application Streamlit.
test_dashboard.py: Script pour les tests unitaires du dashboard.
.gitignore: Fichier spécifiant les fichiers et dossiers à ignorer dans le suivi git.
Procfile: Fichier spécifiant les commandes à exécuter lors du déploiement de l'application sur Heroku.
README.md: Documentation principale du projet.
requirements.txt: Liste des dépendances du projet.
Exigences
Installation
Pour exécuter le code de ce projet, vous aurez besoin de Python 3.11 ou supérieur. Installez les dépendances à l'aide du fichier requirements.txt.

bash
Copy code
pip install -r requirements.txt
Assurez-vous également de personnaliser les chemins et les paramètres dans le fichier config.py selon les besoins de votre projet.

Exécution du script
Pour exécuter le dashboard, assurez-vous d'avoir Python 3.11 ou supérieur installé et exécutez la commande suivante dans le terminal :

bash
Copy code
streamlit run src/dashboard.py

## Structure du Projet

Le projet est organisé de la manière suivante :
- **.github/workflows**: 
  - **tests.yml**: Fichier de configuration pour les workflows GitHub.
- **Data/sampled**: Données sélectionnées pour le déploiement Cloud Heroku.
  - **POS_CASH_balance_selected.csv**
  - **application_train_selected.csv**
  - **bureau_balance_selected.csv**
  - **bureau_selected.csv**
  - **credit_card_balance_selected.csv**
  - **installments_payments_selected.csv**
  - **previous_application_selected.csv**
  - **test_x_selected_head.csv**
- **scr**: Le répertoire principal du code source.
  - **config.py**: Fichier de configuration pour le projet.
  - **data_drift_analysis**: Contient les scripts liés à l'analyse de data drift.
    - **data_drift.py**: Script d'analyse de data drift.
    - **data_drift_report.html**: Rapport HTML généré à partir de l'analyse de data drift.
  - **flask_api.py**: Script principal de l'API Flask.
  - **models**: Contient les scripts liés à la modélisation.
    - **feature_importance.py**: Script pour l'analyse de l'importance des fonctionnalités.
    - **main.py**: Script principal pour le prétraitement et l'entraînement des modèles.
    - **model_training.py**: Script contenant les fonctions d'entraînement des modèles.
    - **models_selec.py**: Script pour la sélection des modèles.
  - **models_saved**: Contient les modèles sauvegardés.
  - **preprocessing**: Scripts pour le prétraitement des données.
    - **aggregation.py**: Script pour l'agrégation des données.
    - **pre_processing.py**: Script pour le nettoyage et l'ingénierie des fonctionnalités.
  - **test_model.py**: Script pour les tests unitaires du modèle.
- **.gitignore**: Fichier spécifiant les fichiers et dossiers à ignorer dans le suivi git.
- **Procfile**: Fichier spécifiant les commandes à exécuter lors du déploiement de l'application.
- **README.md**: Documentation principale du projet.
- **feature_imortance_global.csv**: Fichier CSV contenant l'importance globale des fonctionnalités.
- **makefile**: Fichier de configuration pour la compilation et l'exécution du projet.
- **requirements.txt**: Liste des dépendances du projet.
- **run_tests.sh**: Script pour exécuter les tests du projet sur GitHub.
- **runtime.txt**: Fichier spécifiant la version de Python à utiliser pour le projet.

## Exigences

### Installation

Pour exécuter le code de ce projet, vous aurez besoin de Python 3.11 ou supérieur. Installez les dépendances à l'aide du fichier `requirements.txt`.

```bash
pip install -r requirements.txt
```

Le fichier setup.py est également inclus pour permettre l'installation et la distribution du projet en tant que package Python.
```bash
pip install .
```

### Execution du script
Pour exécuter le script, assurez-vous d'avoir Python 3.11 ou supérieur installé et exécutez la commande suivante dans le terminal :

```bash
python scr/models/main.py
```
Assurez-vous également de personnaliser les chemins et les paramètres dans le fichier [config.py]() selon les besoins de votre projet.
Pour exécuter le code de ce projet, vous aurez besoin de Python 3.11 ou supérieur. Installez les dépendances à l'aide du fichier `requirements.txt`.

```bash
pip install -r requirements.txt
