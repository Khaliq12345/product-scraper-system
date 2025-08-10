from bs4 import BeautifulSoup

class HTMLParser:
    @staticmethod
    def parse_product_data(html_content: str, selectors: dict) -> dict | None:
        if not html_content:
            return None
            
        soup = BeautifulSoup(html_content, 'html5lib')
        
        data = {}
        for key, selector in selectors.items():
            element = soup.select_one(selector) 
            data[key] = element.get_text(strip=True) if element else None
            
        return data