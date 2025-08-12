from typing import Optional
from supabase.client import Client, create_client
from src.config import config


class DataManager:
    def __init__(self) -> None:
        self.supabase: Client = create_client(
            supabase_url=config.SUPABASE_URL, supabase_key=config.SUPABASE_KEY
        )
        self.cache_table = "cacher"

    def get_domain_with_selector(self, domain: str) -> Optional[dict]:
        """Extract domain selector and access type from supabase"""
        response = (
            self.supabase.table(self.cache_table)
            .select("*")
            .eq("domain", domain)
            .execute()
        )
        if response.data:
            return response.data[0]
        return {}

    def save_domain_and_selector(self, data: dict) -> None:
        """Save Domain with the selectors along with the access type"""
        pass

    def save_data(self, data: dict):
        """Save product data to database"""
        pass
