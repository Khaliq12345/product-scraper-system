from typing import Optional, Dict, Any
from supabase.client import create_client, Client
from src.config.config import SUPABASE_URL, SUPABASE_KEY

class DataManager:
    def __init__(self) -> None:
       self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
       self.config_table: str = "cacher"          
       self.data_table: str = "products"          

    def get_domain_with_selector(self, domain: str) -> Optional[Dict[str, Any]]:
        response = self.supabase.table(self.config_table).select('*').eq('domain', domain).execute()
        if response.data:
            return response.data[0]
        return None

    def save_domain_and_selector(self, data: Dict[str, Any]) -> None:
        domain = data.get("domain")
        if not domain:
            raise ValueError("Les données de configuration doivent contenir la clé 'domain'.")
        
        self.supabase.table(self.config_table).upsert(data, on_conflict='domain').execute()

    def save_data(self, data: Dict[str, Any]):
        self.supabase.table(self.data_table).insert(data).execute()