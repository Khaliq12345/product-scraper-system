import sys
from typing import Optional

sys.path.append("..")


from abc import ABC, abstractmethod
from src.core.database_manager import DataManager
from src.core.selector_manager import SelectorManager
from urllib.parse import urlparse


class ScraperBase(ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.database_manager = DataManager()
        self.selector_manager = SelectorManager()
        self.domain=urlparse(self.url).netloc

    @abstractmethod
    def get_html_text(self) -> Optional[str]:
        """Send requests to the specified url and get the html"""
        pass

    def run(self):
        html = self.get_html_text()
        if not html:
            return {}
        
        parsed_data = self.database_manager.get_domain_with_selector(self.domain)
        if parsed_data:
            print(f"Sélecteurs trouvés dans la base de données pour {self.domain}")
        else:
            print(f"Aucun sélecteur trouvé pour {self.domain}. Analyse du HTML...")
            parsed_data = self.selector_manager.parse(html)
            save = parsed_data.copy()
            save["domain"] = self.domain
            save["access_type"] = "request"
            self.database_manager.save_domain_and_selector(save)
            print("Nouveaux sélecteurs sauvegardés dans la base de données.")

        extract_selectors = parsed_data.copy()
        print("Extraction des données à partir du HTML...")
        extracted_data = self.selector_manager.extract_data(html, extract_selectors)

        cleaned_data = {key.replace('_selector', ''): value for key, value in extracted_data.items()}
       
        if 'brand_selector' in cleaned_data:
             cleaned_data['brand'] = cleaned_data.pop('brand_selector')

        db_data = {
            'title': cleaned_data.get('title'),
            'price': cleaned_data.get('price'),
            'brand': cleaned_data.get('brand'),
            'domain': self.domain,
            'link': cleaned_data.get('link'),
            'image': cleaned_data.get('image'), 
            'product': self.url                 
        }

        print(f"Données finales prêtes pour la BDD : {db_data}")
        self.database_manager.save_data(db_data)
        print(" Données du produit sauvegardées avec succès ! ")



        # send selectors and access_type to cache database

        # send data to cache database
