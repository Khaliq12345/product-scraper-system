import sys
from typing import Optional

sys.path.append("..")


from abc import ABC, abstractmethod
from src.core.database_manager import DataManager
from src.core.selector_manager import SelectorManager


class ScraperBase(ABC):
    def __init__(self, url: str, product_id: str) -> None:
        self.url = url
        self.product_id = product_id
        self.database_manager = DataManager()

    @abstractmethod
    def get_html_text(self) -> Optional[str]:
        """Send requests to the specified url and get the html"""
        pass

    def run(self, access_type: str, domain: str, domain_data: dict) -> bool:
        """Start the system"""
        # get the html of the product page
        html = self.get_html_text()
        if not html:
            return False

        self.selector_manager = SelectorManager(html=html)
        self.selector_manager.parse(domain_data)

        # send selectors and access_type to cache database
        selector_output = self.selector_manager.output["selectors"]
        print(selector_output)
        if not selector_output:
            return False
        selector_output["access_type"] = access_type
        selector_output["domain"] = domain
        selector_output["link"] = self.url
        self.database_manager.save_domain_and_selector(selector_output)

        # send data to cache database
        product_output = self.selector_manager.output["values"]
        print(product_output)
        if not product_output:
            return False
        product_output["product_id"] = self.product_id
        product_output["status"] = "success"
        product_output["domain"] = domain
        product_output["link"] = self.url
        self.database_manager.save_data(product_output)

        print("Scraping completed")
        return True
