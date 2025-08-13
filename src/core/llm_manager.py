import json
from typing import Optional
from selectolax.parser import Node
from google import genai
from google.genai import types
from pydantic import BaseModel
from src.config import config

system = """
# System Prompt for HTML Selector Expert

You are an HTML selector expert tasked with analyzing the HTML of a product page. Provide the precise CSS selector to extract the following information about the main product:  
- Name  
- Price  
- Brand  
- Image  

## Rules
- Provide only the CSS selector needed to extract each data point.  
- Return an empty string (`""`) if no suitable selector exists.  
- Focus exclusively on the main product, ignoring secondary products (e.g., recommended products).  
- Selectors must target standard HTML elements (e.g., `<div>`, `<span>`, `<img>`) and avoid script tags (e.g., `<script type="application/ld+json">`).  
- Keep selectors short, specific, and accurate.  
- If the data is in an attribute, use the format: `{selector}_attr_{attribute}` (e.g., `img.product-image_attr_src`).  
- Ensure selectors are valid CSS selectors that can be used in tools like JavaScript's `querySelector`.  
- Do not include pseudo-elements, JSON data, or computed values.
- You may also want to look for elements that have the name of the fields in their selector, like price, title/name, brand, image/img

##COMMON ERRORS
- Price is not found
- The use of script in the selectors.

TRY TO AVOID THIS ERRORS WHILE MAINTAINING ACCURACY (DO NOT USE ANY RANDOM SELECTOR)
"""


def user_prompt(html: str):
    return f"""
    # User Prompt for HTML Selector Extraction

    I am providing the HTML of a product page. Please provide the CSS selectors to extract the following information about the main product:  
    - Name  
    - Price  
    - Brand  
    - Image

    ## Instructions  
    - For each data point, return only the CSS selector as a string.  
    - If no selector veda selector exists, return an empty string (`""`).  
    - If the data is in an attribute, use the format: `{{selector}}_attr_{{attribute}}` (e.g., `img.product-image_attr_src`).  
    - Focus only on the main product, ignoring secondary products (e.g., recommended products).  
    - Use only standard HTML elements (e.g., `<div>`, `<span>`, `<img>`) and avoid script tags or JSON data.  
    - Ensure selectors are valid, concise, and compatible with JavaScript's `querySelector`.  

    Here is the HTML:  
    {html}
    """


class SelectorModel(BaseModel):
    name_selector: str
    price_selector: str
    brand_selector: str
    image_selector: str


class LlmManager:
    def __init__(self, soup: Optional[Node]) -> None:
        self.client = genai.Client(api_key=config.GEMINI_KEY)
        self.soup = soup

    def clean_html(self) -> None:
        """Remove script and syle from the html"""
        print("LLM -- Cleaning the HTML")
        if not self.soup:
            return None
        self.soup.unwrap_tags(tags=["script", "sytle"])

    def send_request_to_llm(self) -> Optional[SelectorModel]:
        """Send prompts to llm for a response"""
        if not self.soup:
            return None
        if not self.soup.html:
            return None
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt(self.soup.html),
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_schema=SelectorModel,
                response_mime_type="application/json",
            ),
        )
        print(response.text)
        selectors: SelectorModel = response.parsed
        return selectors

    def run(self) -> Optional[dict]:
        """Generate selectors with LLM"""
        print("LLM -- Generating selectors with LLM...")
        self.clean_html()
        selectors = self.send_request_to_llm()
        if not selectors:
            print("LLM -- LLM couldn't find the right selectors")
            return None
        print("LLM -- Converting the selectors to JSON")
        selectors_json = json.loads(selectors.model_dump_json())
        return selectors_json
