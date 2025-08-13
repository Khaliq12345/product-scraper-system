from typing import Dict
from gotrue import Optional
from selectolax.parser import HTMLParser
from src.core.llm_manager import LlmManager
##Note for the llm, remove all script and other things that won't be needed for the parsing


class SelectorManager:
    def __init__(self, html: str) -> None:
        self.html = html
        self.html_node = HTMLParser(html)
        self.llm_manager = LlmManager(self.html_node.body)
        self.output = {}
        self.output["selectors"] = {}
        self.output["values"] = {}

    def selector_to_text(
        self, selector: str, name: str, attribute: Optional[str] = None
    ) -> Optional[str]:
        """Extract text and selector save from node"""
        node = self.html_node.css_first(selector)
        if node:
            # save the seletors alongside the value
            if not attribute:
                value = node.text(separator=" ", strip=True)
                self.output["selectors"][f"{name}_selector"] = {
                    "selector": selector,
                    "attribute": None,
                }
                self.output["values"][name] = value
                return value
            else:
                value = node.attributes[attribute]
                self.output["selectors"][f"{name}_selector"] = {
                    "selector": selector,
                    "attribute": attribute,
                }
                self.output["values"][name] = value
                return value
        return None

    def llm_selector_text(self, selector: str, name: str) -> Optional[str]:
        # # Extract data using distinct selectors
        if not selector:
            return None
        value_attr = selector.split("_attr_")
        if len(value_attr) > 1:
            return self.selector_to_text(
                selector=value_attr[0], attribute=value_attr[1], name=name
            )
        elif len(value_attr) > 0:
            return self.selector_to_text(value_attr[0], name=name)

    def parse(self) -> None:
        """Parse html to dictionary"""
        print("SELECTOR MANAGER -- Extracting selector for a new domain")
        parsed_dict: Dict[str, Optional[str]] = {
            "name": None,
            "price": None,
            "image": None,
            "brand": None,
        }
        selectors_values = None
        parsed_dict["name"] = self.selector_to_text(
            'meta[property="og:title"]', attribute="content", name="name"
        )
        parsed_dict["price"] = self.selector_to_text(
            'meta[property="og:price"]', attribute="content", name="price"
        )
        parsed_dict["image"] = self.selector_to_text(
            'meta[property="og:image"]', attribute="content", name="image"
        )
        parsed_dict["brand"] = self.selector_to_text(
            'meta[propert="og:brand"]', attribute="content", name="brand"
        )
        for key in parsed_dict:
            if not parsed_dict[key]:
                print(
                    "SELECTOR MANAGER -- Meta parsing is incomplete or unavailable. Fallback to LLM"
                )
                selectors_values = self.llm_manager.run()
                break

        if selectors_values:
            print(selectors_values)
            for key in parsed_dict:
                parsed_dict[key] = (
                    parsed_dict[key]
                    if parsed_dict[key]
                    else self.llm_selector_text(
                        selectors_values[f"{key}_selector"], key
                    )
                )

        return None
