"""
Script de Test pour Recherche_client.py

Ce script contient des tests unitaires pour les fonctions définies dans Recherche_client.py.
Les tests couvrent des fonctionnalités liées à la gestion des valeurs NaN, à l'obtention d'informations sur le client,
et à la simulation de récupération de données à des fins de test.

Fonctions:
    - test_valid_page(): Teste la validité de la page du tableau de bord Streamlit.
    - test_replace_nan_with_none(): Teste la fonction replace_nan_with_none.
    - sample_data(): Fonction fixture pour créer des données fictives pour les tests.
    - test_get_client_info(): Teste la fonction get_client_info en utilisant des données fictives.
    - test_obtain_raw_client_info(): Teste la fonction obtain_raw_client_info en utilisant des données fictives.
    - test_obtain_info_by_table(): Teste la fonction obtain_info_by_table avec des données simulées.
    - test_get_client_info_not_found(): Teste la fonction get_client_info avec un ID client inexistant.
"""
import pandas as pd 
import pytest
from streamlit.testing.v1 import AppTest
from Recherche_client import (
    replace_nan_with_none,
    obtain_info_by_table,
    obtain_raw_client_info,
    get_client_info,
)

def test_valid_page():
    """
    Teste la validité de la page du tableau de bord Streamlit.
    """
    at = AppTest.from_file("Recherche_client.py").run()
    assert not at.exception

def test_replace_nan_with_none():
    """
    Teste la fonction replace_nan_with_none.
    """
    d = {'a': 1, 'b': None, 'c': 3}
    result = replace_nan_with_none(d)
    assert result == {'a': 1, 'b': None, 'c': 3}

@pytest.fixture
def sample_data():
    """
    Fonction fixture pour créer des données fictives pour les tests.
    """
    data = pd.DataFrame({
        'SK_ID_CURR': [123, 456, 789],
        'Name': ['John Doe', 'Jane Doe', 'Bob Smith'],
        'Age': [30, 25, 40],
    })
    return data

def test_get_client_info(sample_data):
    """
    Teste la fonction get_client_info en utilisant des données fictives.
    """
    client_id = 456
    client_info = get_client_info(client_id, sample_data)

    assert isinstance(client_info, dict)
    assert "error" not in client_info
    assert client_info['SK_ID_CURR'] == 456
    assert client_info['Name'] == 'Jane Doe'
    assert client_info['Age'] == 25

def test_obtain_raw_client_info():
    """
    Teste la fonction obtain_raw_client_info en utilisant des données fictives.
    """
    client_id = 456
    client_info = obtain_raw_client_info(client_id)

    assert isinstance(client_info, dict)
    assert 'informations_application' in client_info
    assert 'informations_bureau' in client_info
    assert 'informations_previous_application' in client_info

def test_obtain_info_by_table(monkeypatch, sample_data):
    """
    Teste la fonction obtain_info_by_table avec des données simulées.
    """
    client_id = 123
    expected_result = [
        {"SK_ID_CURR": 123, "Name": 'John Doe', "Age": 30},
    ]

    monkeypatch.setattr("pandas.read_csv", lambda x: sample_data)
    result = obtain_info_by_table("mock_url.csv", client_id)

    assert result == expected_result

def test_get_client_info_not_found(sample_data):
    """
    Teste la fonction get_client_info avec un ID client inexistant.
    """
    client_id = 999
    client_info = get_client_info(client_id, sample_data)

    assert isinstance(client_info, dict)
    assert "error" in client_info
    assert client_info['error'] == 'Client non trouvé'
