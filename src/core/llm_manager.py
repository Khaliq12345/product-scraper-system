from clean_html_for_llm import clean_html
import json
from typing import Optional
from google import genai
from google.genai import types
from pydantic import BaseModel
from src.config import config

selector_system_prompt = """
# System Prompt for HTML Selector Expert

You are an expert in CSS selectors tasked with analyzing the raw HTML of a product detail page to extract selectors for the main product's details. Given the raw HTML, provide precise CSS selectors for the following data points:
- Product Name
- Product Price (the final price the customer pays, e.g., discounted price if available)
- Brand
- Main Product Image (the URL of the primary image, typically from an `<img>` tag's `src` attribute)

## Rules
1. Analyze the raw HTML and identify the most specific, stable, and unique CSS selectors for each data point that will consistently extract the correct value.
2. Focus exclusively on the main product, ignoring secondary products (e.g., recommended products, upsells, or related items).
3. Use only standard HTML elements (e.g., `<div>`, `<span>`, `<img>`) and avoid script tags (e.g., `<script type="application/ld+json">`), JSON data, or computed values.
4. For the image, provide a selector for the `<img>` tag’s `src` attribute in the format: `{selector}_attr_src` (e.g., `img.product-image_attr_src`).
5. For the price, select the final customer-facing price (e.g., discounted price over regular price). If multiple prices exist, choose the most prominent (e.g., largest font, highlighted, or marked as current) and explain your choice in the `notes` field.
6. Prioritize selectors that include keywords like `name`, `title`, `price`, `brand`, `image`, or `img` in class names, IDs, or attributes (e.g., `data-testid`, `id`, `class="product-price"`). Avoid dynamic or generated class names (e.g., `sc-123abc`).
7. Ensure selectors are concise, specific, and compatible with JavaScript’s `querySelector`.
8. If no selector can be found for a data point or the data is unavailable (e.g., JavaScript-rendered), return an empty string (`""`) for the selector and provide a reason in the `notes` field (e.g., "Price likely JavaScript-rendered").
9. Bad CSS Selectors
"""


def selector_user_prompt(html: str):
    return f"""
    # User Prompt for HTML Selector Extraction
    
    # Make sure to follow the system rules

    ## HTML
    ```html
    {html}
    ```
    """


data_cleaning_system_prompt = """
You are an expert data cleaning assistant for e-commerce product data. Your task is to clean and standardize product data provided in JSON format, including product name, price, brand, and image URL, for database storage. Use the following rules to ensure consistent, accurate output:

## Cleaning Rules
1. **Product Name**:
   - Keep the core product description (e.g., "Samba OG Shoes"), removing marketing terms (e.g., "Free Shipping", "Ideal for Gift"), colors (e.g., "White"), or site-specific details (e.g., "adidas US").
   - Remove special characters (e.g., "!!!", "**") unless essential to the product name.
   - Limit to 50 characters if possible, without losing key details.
   - Use title case (e.g., "Adidas Samba OG Shoes").
   - If the brand appears in the name, ensure it matches the brand field or extract it if brand is missing.

2. **Price**:
   - Remove currency symbols (e.g., "$", "€", "£") and text (e.g., "USD").
   - Convert to a string float (e.g., "$100" to "100.00", "$31.18" to "31.18").
   - For price ranges (e.g., "$80-$100"), use the lowest value.

3. **Brand**:
   - Clean to title case (e.g., "ADIDAS" to "Adidas"), removing redundant terms (e.g., "Inc.").
   - If missing or empty, extract from the product name (e.g., "adidas" from "adidas Samba OG Shoes").
   - If no brand is in the name, use the domain (e.g., "adidas.com" becomes "Adidas") as a fallback.
   - If no brand can be determined, return "" and explain in `notes`.

4. **Image**:
   - Keep valid URLs (starting with "http" or "https", ending with ".jpg", ".png", etc.).
   - If missing, invalid, or empty, return "" and explain in `notes`.

6. **Constraints for Gemini-2.5-Flash**:
   - Be precise and avoid ambiguity, as the model has limited context understanding.
   - If data is unclear, make a best guess and document in `notes`.
   - Keep processing simple to minimize errors.

## Common Errors to Avoid
- Do not return empty values unless explicitly justified (e.g., missing data).
- Avoid removing essential product details (e.g., "Samba OG Shoes" is core).
- Do not confuse generic terms (e.g., "Shoes") with brands.
"""


def cleaned_data_user_prompt(product_dict: dict):
    return f"""
        Clean the following product data according to the system rules.
        Return the cleaned data in JSON format with values and notes for each field (name, price, brand, image).

        ## Cleaning Rules
        1. **Product Name**:
           - Keep the core product description (e.g., "Samba OG Shoes"), removing marketing terms (e.g., "Free Shipping", "Ideal for Gift"), colors (e.g., "White"), or site-specific details (e.g., "adidas US").
           - Remove special characters (e.g., "!!!", "**") unless essential to the product name.
           - Limit to 50 characters if possible, without losing key details.
           - Use title case (e.g., "Adidas Samba OG Shoes").
           - If the brand appears in the name, ensure it matches the brand field or extract it if brand is missing.

        2. **Price**:
           - Remove currency symbols (e.g., "$", "€", "£") and text (e.g., "USD").
           - Convert to a string float (e.g., "$100" to "100.00", "$31.18" to "31.18").
           - For price ranges (e.g., "$80-$100"), use the lowest value.

        3. **Brand**:
           - Clean to title case (e.g., "ADIDAS" to "Adidas"), removing redundant terms (e.g., "Inc.").
           - If missing or empty, extract from the product name (e.g., "adidas" from "adidas Samba OG Shoes").
           - If no brand is in the name, use the domain (e.g., "adidas.com" becomes "Adidas") as a fallback.
           - If no brand can be determined, return "" and explain in `notes`.

        4. **Image**:
           - Keep valid URLs (starting with "http" or "https", ending with ".jpg", ".png", etc.).
           - If missing, invalid, or empty, return "" and explain in `notes`.

        6. **Constraints for Gemini-2.5-Flash**:
           - Be precise and avoid ambiguity, as the model has limited context understanding.
           - If data is unclear, make a best guess and document in `notes`.
           - Keep processing simple to minimize errors.

        ## Common Errors to Avoid
        - Do not return empty values unless explicitly justified (e.g., missing data).
        - Avoid removing essential product details (e.g., "Samba OG Shoes" is core).
        - Do not confuse generic terms (e.g., "Shoes") with brands.

        **Input Data**:
        {product_dict}
        """


class SelectorModel(BaseModel):
    name_selector: str
    price_selector: str
    brand_selector: str
    image_selector: str


class ProductModel(BaseModel):
    name: str
    price: str
    brand: str
    image: str


class LlmManager:
    def __init__(self, body_html: str) -> None:
        self.client = genai.Client(api_key=config.GEMINI_KEY)
        self.html = body_html
        self.html_cleaner()

    def html_cleaner(self) -> None:
        """Remove script and syle from the html"""
        print("LLM -- Cleaning the HTML")
        self.html = clean_html(self.html)
        print(f"Total - {len(self.html)}")

    def send_request_to_llm(self) -> Optional[SelectorModel]:
        """Send prompts to llm for a response"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=selector_user_prompt(self.html),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SelectorModel,
                system_instruction=selector_system_prompt,
            ),
        )
        selectors: SelectorModel = response.parsed
        return selectors

    def get_selectors(self) -> Optional[dict]:
        """Generate selectors with LLM"""
        print("LLM -- Generating selectors with LLM...")
        selectors = self.send_request_to_llm()
        if not selectors:
            print("LLM -- LLM couldn't find the right selectors")
            return None
        print("LLM -- Converting the selectors to JSON")
        selectors_json = json.loads(selectors.model_dump_json())
        return selectors_json

    def clean_data(self, input_dict: dict) -> Optional[dict]:
        """Clean the input data"""
        print("LLM -- Cleaning data")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=cleaned_data_user_prompt(input_dict),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProductModel,
                system_instruction=data_cleaning_system_prompt,
            ),
        )
        product: ProductModel = response.parsed
        return json.loads(product.model_dump_json())
