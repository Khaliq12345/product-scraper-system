import pytest
from dotenv import load_dotenv
from core.database_manager import DataManager

load_dotenv()

TEST_DOMAIN_CONFIG = {
    "domain": "test1.com",
    "access_type": "requests",
    "selector_title": "h1.title",
    "selector_price": ".price",
    "selector_image": "img.product-image",
    "brand_selector": ".brand-name",
    "link": "a.product-link"

}

TEST_PRODUCT_DATA = {
    "title": "Un produit de test",
    "price": 99.99,
    "image_url": "https://test.com/image.jpg",
    "brand": "TestBrand",
    "product_url": "https://test.com/product/1234",
    "domain":"test.com"
}

def test_integration_save_domain_config():
    """
    Test d’intégration : envoie de la config réelle dans la table 'cacher'.
    """
    db_manager = DataManager()
    try:
        db_manager.save_domain_and_selector(TEST_DOMAIN_CONFIG)
    except Exception as e:
        pytest.fail(f"Échec lors de save_domain_and_selector : {e}")

def test_integration_save_product_data():
    """
    Test d’intégration : envoie de données produit réelles dans la table 'products'.
    """
    db_manager = DataManager()
    try:
        db_manager.save_data(TEST_PRODUCT_DATA)
    except Exception as e:
        pytest.fail(f"Échec lors de save_data : {e}")
