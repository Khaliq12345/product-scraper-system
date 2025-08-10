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
        self.selector_manager = SelectorManager()

    @abstractmethod
    def get_html_text(self) -> Optional[str]:
        """Send requests to the specified url and get the html"""
        pass

    def run(self):
        html = self.get_html_text()
        if not html:
            return {}
        parsed_data = self.selector_manager.parse(html)

        # send selectors and access_type to cache database

        # send data to cache database
