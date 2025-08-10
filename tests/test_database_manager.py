

import pytest
from unittest.mock import MagicMock


from core.database_manager import DataManager


TEST_DOMAIN_CONFIG = {
    "domain": "test.com",
    "access_type": "requests",
    "selector_title": "h1.title",
    "selector_price": ".price"
}

TEST_PRODUCT_DATA = {
    "title": "Un produit de test",
    "price": 99.99
}


def test_get_domain_with_selector_success(mocker):
    """ Test : domaine trouvé dans la table 'cacher' """
    mock_response = MagicMock()
    mock_response.data = [TEST_DOMAIN_CONFIG]

    mock_supabase_client = MagicMock()
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
    
    mocker.patch('core.database_manager.create_client', return_value=mock_supabase_client)

    db_manager = DataManager()
    result = db_manager.get_domain_with_selector("test.com")

    mock_supabase_client.table.assert_called_with('cacher')
    mock_supabase_client.table().select().eq.assert_called_with('domain', 'test.com')
    assert result == TEST_DOMAIN_CONFIG


def test_get_domain_with_selector_not_found(mocker):
    """ Test : domaine non trouvé, la fonction doit retourner None """
    mock_response = MagicMock()
    mock_response.data = []

    mock_supabase_client = MagicMock()
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    mocker.patch('core.database_manager.create_client', return_value=mock_supabase_client)

    db_manager = DataManager()
    result = db_manager.get_domain_with_selector("unknown.com")

    assert result is None


def test_save_domain_and_selector(mocker):
    """ Test : sauvegarde ou mise à jour d'un domaine et ses sélecteurs """
    mock_supabase_client = MagicMock()
    mocker.patch('core.database_manager.create_client', return_value=mock_supabase_client)

    db_manager = DataManager()
    db_manager.save_domain_and_selector(TEST_DOMAIN_CONFIG)

    mock_supabase_client.table.assert_called_with('cacher')
    mock_supabase_client.table().upsert.assert_called_once_with(
        TEST_DOMAIN_CONFIG,
        on_conflict='domain'
    )


def test_save_domain_and_selector_raises_error_if_no_domain():
    """ Test : la sauvegarde échoue si la clé 'domain' est absente """
    db_manager = DataManager()
    with pytest.raises(ValueError, match="doivent contenir la clé 'domain'"):
        db_manager.save_domain_and_selector({"un champ": "une valeur"})


def test_save_data(mocker):
    """ Test : insertion des données produit dans la table 'products' """
    mock_supabase_client = MagicMock()
    mocker.patch('core.database_manager.create_client', return_value=mock_supabase_client)

    db_manager = DataManager()
    db_manager.save_data(TEST_PRODUCT_DATA)

    mock_supabase_client.table.assert_called_with('products')
    mock_supabase_client.table().insert.assert_called_once_with(TEST_PRODUCT_DATA)


@pytest.mark.integration
def test_integration_save_domain_config():
    """
    [TEST D'INTÉGRATION]
    Envoie des données de configuration RÉELLES à la table 'cacher' sur Supabase.
    Nécessite un fichier .env valide et une connexion internet.
    """
    print("\n[INTÉGRATION] Envoi des données de configuration à la VRAIE base de données...")
    try:
        db_manager = DataManager()
        db_manager.save_domain_and_selector(TEST_DOMAIN_CONFIG)
        print("    [INTÉGRATION] Données de configuration envoyées avec succès !")
    except Exception as e:
        pytest.fail(f"Le test d'intégration pour save_domain_and_selector a échoué : {e}")

@pytest.mark.integration
def test_integration_save_product_data():
    """
    [TEST D'INTÉGRATION]
    Envoie des données produit RÉELLES à la table 'products' sur Supabase.
    """
    print("\n[INTÉGRATION] Envoi des données produit à la VRAIE base de données...")
    try:
        db_manager = DataManager()
        db_manager.save_data(TEST_PRODUCT_DATA)
        print("   ✅ [INTÉGRATION] Données produit envoyées avec succès !")
    except Exception as e:
        pytest.fail(f"Le test d'intégration pour save_data a échoué : {e}")