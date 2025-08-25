import sys
from typing import Optional

sys.path.append("..")

from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from src.core.scraper import ScraperBase


class DynamicScraper(ScraperBase):
    def __init__(self, url: str, product_id: str) -> None:
        super().__init__(url, product_id)

    def get_html_text(self) -> Optional[str]:
        """Extract html using simple requests"""
        with sync_playwright() as playwright:
            launcher = playwright.firefox
            browser = launcher.launch(headless=False)
            page = browser.new_page()
            page.goto(self.url, timeout=120000)
            page.wait_for_timeout(10000)
            content = page.content()
            soup = HTMLParser(content)
            browser.close()
            return soup.html
