from selectolax.parser import HTMLParser


class SelectorManager:
    def __init__(self) -> None:
        pass

    def parse_soup_with_meta(self, soup: HTMLParser):
        """Extract the data with popular metadata and save to db"""
        pass

    def parse_soup_with_llm(self, soup: HTMLParser):
        """Extract the data with llm and save to db"""
        pass

    def parse(self, html: str) -> dict:
        """Parse html to dictionnary"""
        soup = HTMLParser(html)
        return {}
