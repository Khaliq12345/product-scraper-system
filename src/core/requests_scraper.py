import sys
from typing import Optional

sys.path.append("..")

import hrequests
from selectolax.parser import HTMLParser
from src.core.scraper import ScraperBase


class StaticScraper(ScraperBase):
    def __init__(self, url: str, product_id: str) -> None:
        super().__init__(url, product_id)

    def get_html_text(self) -> Optional[str]:
        """Extract html using simple requests"""
        with hrequests.Session() as session:
            resp = session.get(self.url)
            print(f"Status code - {resp.status_code}")
            if resp.status_code != 200:
                return None
            soup = HTMLParser(resp.text)
            return soup.html
