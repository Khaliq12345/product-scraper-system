import sys
from typing import Optional

sys.path.append("..")

import hrequests
from selectolax.parser import HTMLParser
from src.core.scraper import ScraperBase


class StaticScraper(ScraperBase):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def get_html_text(self) -> Optional[str]:
        with hrequests.Session() as session:
            resp = session.get(self.url)
            if resp.status_code >= 400:
             raise Exception(f"HTTP Error {resp.status_code} for URL: {self.url}")
            soup = HTMLParser(resp.text)
            return soup.html
