from typing import Optional
from supabase.client import Client, create_client
from src.config import config


class DataManager:
    def __init__(self) -> None:
        self.supabase: Client = create_client(
            supabase_url=config.SUPABASE_URL, supabase_key=config.SUPABASE_KEY
        )
        self.cache_table = "cacher"
        self.product_table = "products"

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
        self.supabase.table(self.cache_table).upsert(
            data, on_conflict="domain"
        ).execute()

    def save_data(self, data: dict):
        """Save product data to database"""
        self.supabase.table(self.product_table).update(data).eq(
            "product_id", data["product_id"]
        ).execute()

    def get_product_info(self, product_id: str) -> Optional[dict]:
        """Get product data from supabase"""
        response = (
            self.supabase.table(self.product_table)
            .select("*")
            .eq("product_id", product_id)
            .execute()
        )
        if response.data:
            return response.data[0]

    def update_product_status(self, product_id: str, status: str) -> None:
        """Change the status of a product in the db"""
        self.supabase.table(self.product_table).upsert(
            {"status": status, "product_id": product_id}, on_conflict="product_id"
        ).execute()
