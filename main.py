# in main.py

from urllib.parse import urlparse
from src.core.database_manager import DatabaseManager
from src.core.requests_scraper import HTTPManager
from src.core.scraper import HTMLParser

class ProductScraperApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.http_manager = HTTPManager()
        self.html_parser = HTMLParser()

    def run(self, url: str):
        domain = urlparse(url).netloc
        print(f"--- Début du traitement pour l'URL : {url} ---")
        print(f"Domaine détecté : {domain}")

        selectors = self.db_manager.get_selectors_by_domain(domain)
        
        if selectors and selectors.get('title'):
            self._process_known_domain(url, domain, selectors)
        else:
            self._process_unknown_domain(domain)
        
        print(f"--- Fin du traitement pour l'URL : {url} ---\n")

    def _process_known_domain(self, url: str, domain: str, selectors: dict):
        print(f"Sélecteurs trouvés dans 'cacher' pour le domaine {domain}. Lancement du scraping.")
        html = self.http_manager.fetch_html(url)
        if not html:
            print("Échec de la récupération du HTML. Opération annulée.")
            return

        product_data = self.html_parser.parse_product_data(html, selectors)
        
        if product_data and product_data.get('title'):
            data_to_save = {
                "source_url": url,
                "domain": domain,
                "title": product_data.get('title'),
                "price": product_data.get('price'),
                "image_url": product_data.get('image_url')
            }
            self.db_manager.save_product_data(data_to_save)
        else:
            print("Le scraping n'a retourné aucune donnée valide. La sauvegarde est annulée.")

    def _process_unknown_domain(self, domain: str):
        print(f"Aucun sélecteur valide trouvé dans la table 'cacher' pour le domaine {domain}.")
        print("Veuillez ajouter les sélecteurs pour ce domaine dans la base de données.")

def main():
    target_url = "https://www.adoredvintage.com/products/classic-effortless-blue-natural-striped-linen-shorts"
    
    print(f"URL de test définie dans le script : {target_url}")
    
    try:
        app = ProductScraperApp()
        app.run(target_url)
    except Exception as e:
        print(f"Une erreur critique est survenue dans l'application : {e}")

if __name__ == "__main__":
    main()