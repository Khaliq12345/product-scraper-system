import sys
from typing import Optional

sys.path.append("..")


from abc import ABC, abstractmethod
from src.core.database_manager import DataManager
from src.core.selector_manager import SelectorManager


class ScraperBase(ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.database_manager = DataManager()

    @abstractmethod
    def get_html_text(self) -> Optional[str]:
        """Send requests to the specified url and get the html"""
        pass

    def run(self) -> bool:
        html = self.get_html_text()
        if not html:
            return False

        self.selector_manager = SelectorManager(html=html)
        self.selector_manager.parse()
        print(self.selector_manager.output)

        # send selectors and access_type to cache database

        # send data to cache database

        print("Scraping completed")
        return True
