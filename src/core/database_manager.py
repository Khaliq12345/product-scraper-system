from typing import Optional
from supabase.client import create_client


class DataManager:
    def __init__(self) -> None:
        pass

    def get_domain_with_selector(self, domain: str) -> Optional[dict]:
        """Extract domain selector and access type from supabase"""
        pass

    def save_domain_and_selector(self, data: dict) -> None:
        """Save Domain with the selectors along with the access type"""
        pass

    def save_data(self, data: dict):
        """Save product data to database"""
        pass
