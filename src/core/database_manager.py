from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY

class DatabaseManager:
    
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Les clés Supabase URL et API Key ne sont pas définies.")
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_selectors_by_domain(self, domain: str) -> dict | None:
       
        try:
           
            response = self.client.table('cacher').select(
                "selector_title, selector_price, selector_image"
            ).eq(
                'domain', domain
            ).not_.is_(
                'selector_title', 'NULL'
            ).limit(1).execute()

            if response.data:
                result = response.data[0]
                return {
                    "title": result['selector_title'],
                    "price": result['selector_price'],
                    "image": result['selector_image']
                }
        except Exception as e:
            print(f"Erreur lors de la récupération des sélecteurs depuis 'cacher' : {e}")
        return None

    def save_product_data(self, product_data: dict):
        """
        Sauvegarde les données d'un produit dans la table 'scraped_products'.
        """
        try:
            
            self.client.table('scraped_products').upsert(product_data).execute()
            print("Produit sauvegardé avec succès dans 'scraped_products'.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du produit : {e}")
            
    def save_selectors_for_domain(self, selector_data: dict):
       
        try:
            print(f"Sauvegarde des nouveaux sélecteurs pour le domaine {selector_data.get('domain')}...")
            self.client.table('cacher').upsert(selector_data).execute()
            print("Sélecteurs sauvegardés avec succès dans 'cacher'.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des sélecteurs : {e}")