from typing import Dict
from gotrue import Optional
from selectolax.parser import HTMLParser

##Note for the llm, remove all script and other things that won't be needed for the parsing


class SelectorManager:
    def __init__(self, html: str) -> None:
        self.html = html
        self.html_node = HTMLParser(html)

    def selector_to_text(
        self, selector: str, attribute: Optional[str] = None
    ) -> Optional[str]:
        """Extract text from node"""
        node = self.html_node.css_first(selector)
        if node:
            if not attribute:
                return node.text(separator=" ", strip=True)
            else:
                return node.attributes[attribute]
        return None

    def llm_to_text(self, selector_type: str):
        """Use LLM to extract data"""
        pass

    def parse_soup_with_meta(self):
        """Extract the data with popular metadata and save to db"""
        pass

    def parse_soup_with_llm(self):
        """Extract the data with llm and save to db"""
        pass

    def parse(self) -> dict:
        """Parse html to dictionary"""
        parsed_dict: Dict[str, Optional[str]] = {
            "name": None,
            "price": None,
            "image": None,
            "brand": None,
        }
        parsed_dict["name"] = self.selector_to_text(
            'meta[property="og:title"]', attribute="content"
        )
        parsed_dict["price"] = self.selector_to_text(
            'meta[property="og:price"]', attribute="content"
        )
        parsed_dict["image"] = self.selector_to_text(
            'meta[property="og:image"]', attribute="content"
        )
        parsed_dict["brand"] = self.selector_to_text(
            'meta[propert="og:brand"]', attribute="content"
        )
        print(parsed_dict)
        return {}
