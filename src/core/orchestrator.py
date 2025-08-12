import sys

sys.path.append("..")

from src.core.database_manager import DataManager
from src.core.requests_scraper import StaticScraper
from urllib.parse import urlparse


class Orchestrator:
    def __init__(self, url: str) -> None:
        self.database = DataManager()
        self.static_scraper = StaticScraper(url)
        self.url = url
        self.domain = urlparse(url).netloc

    def past_domain_handler(self, domain_data: dict):
        """Use cached info to handle data"""
        pass

    def new_domain_handler(self) -> None:
        """Handle new domain"""
        print("New domain deteced - Trying the static method")
        is_done = self.static_scraper.run()
        if not is_done:
            print("Fallback to browser method")
            # run the browser scraper
            pass
        return None

    def main(self):
        """Verify if there's cache and passe it to the right scraper"""
        domain_data = self.database.get_domain_with_selector(self.domain)
        print(domain_data)
        if domain_data:
            # use saved access_type and selector to handle it
            pass
        else:
            self.new_domain_handler()


if __name__ == "__main__":
    url = "https://www.acmetools.com/bosch-18v-brushless-9-inch-cutoff-saw-kit-gcs18v-230n212/S0000000088753.html"
    runner = Orchestrator(url)
    runner.main()
