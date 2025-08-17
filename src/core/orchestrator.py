import sys
from typing import Optional

sys.path.append("..")

from src.core.database_manager import DataManager
from src.core.requests_scraper import StaticScraper
from urllib.parse import urlparse


class Orchestrator:
    def __init__(self, url: str, product_id: str) -> None:
        self.product_id = product_id
        self.database = DataManager()
        self.static_scraper = StaticScraper(url, product_id)
        self.url = url
        self.domain = urlparse(url).netloc

    def past_domain_handler(self, domain_data: dict) -> Optional[bool]:
        """Use cached info to handle data"""
        print(
            f"Domain deteced in cache - Trying the {domain_data['access_type']} method"
        )
        is_done = False
        if domain_data["access_type"] == "static":
            is_done = self.static_scraper.run(
                "static", self.domain, domain_data
            )
        elif domain_data["access_type"] == "dynamic":
            is_done = False
        return is_done

    def new_domain_handler(self) -> Optional[bool]:
        """Handle new domain"""
        print("New domain deteced - Trying the static method")
        access_type = "static"
        is_done = self.static_scraper.run(access_type, self.domain, {})
        if not is_done:
            access_type = "dynamic"
            print("Fallback to browser method")
            # run the browser scraper
            pass
        return is_done

    def main(self):
        """Verify if there's cache and passe it to the right scraper"""
        is_done = False
        # update status to running
        self.database.update_product_status(self.product_id, "running")
        try:
            domain_data = self.database.get_domain_with_selector(self.domain)
            # print(domain_data)
            if domain_data:
                # use saved access_type and selector to handle it
                is_done = self.past_domain_handler(domain_data)
            else:
                is_done = self.new_domain_handler()
        except Exception as e:
            print(f"Error - {e}")
            is_done = False
        if not is_done:
            self.database.update_product_status(self.product_id, "failed")


if __name__ == "__main__":
    url = "https://www.albanypark.com/collections/barton/products/barton-sofa?variant=41412605607987"
    runner = Orchestrator(url, "testId")
    runner.main()
