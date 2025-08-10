
from bs4 import BeautifulSoup

class SelectorManager:
   
    def extract_data(self, soup: BeautifulSoup, selectors_config: dict) -> dict:
       
        print("[SelectorManager] - Démarrage de l'extraction des données.")
        if not soup:
            print("[SelectorManager] - ERREUR : La 'soupe' HTML est vide.")
            return {}

        results = {}
        for data_name, config in selectors_config.items():
            selector = config.get('selector')
            extract_type = config.get('type', 'single') 

            if not selector:
                continue

            if extract_type == 'single':
                element = soup.select_one(selector)
                results[data_name] = element.get_text(strip=True) if element else None
            
            elif extract_type == 'multiple':
                elements = soup.select(selector)
                results[data_name] = [el.get_text(strip=True) for el in elements]

        print("[SelectorManager] - Extraction terminée.")
        return results