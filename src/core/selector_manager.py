from selectolax.parser import HTMLParser
from typing import Dict,Optional,Any

class SelectorManager:
    def __init__(self) -> None:
        pass

    def parse_soup_with_meta(self, soup: HTMLParser) -> Dict[str, Optional[str]]:
        selectors = {}

        if soup.css_first('meta[property="og:title"]'):
            selectors['selector_title'] = 'meta[property="og:title"]'
        elif soup.css_first('title'):
            selectors['selector_title'] = 'title'

        if soup.css_first('meta[property="product:price:amount"]'):
            selectors['selector_price'] = 'meta[property="product:price:amount"]'
        elif soup.css_first('meta[itemprop="price"]'):
            selectors['selector_price'] = 'meta[itemprop="price"]'
        elif soup.css_first('[class*="price"], [id*="price"], [itemprop*="price"]'):
            selectors['selector_price'] = '[class*="price"], [id*="price"], [itemprop*="price"]'

        if soup.css_first('meta[property="og:image"]'):
            selectors['selector_image'] = 'meta[property="og:image"]'
        elif soup.css_first('img[itemprop="image"]'):
            selectors['selector_image'] = 'img[itemprop="image"]'
        elif soup.css_first('img[class*="product"], img[id*="product"], img[alt*="product"]'):
            selectors['selector_image'] = 'img[class*="product"], img[id*="product"], img[alt*="product"]'

        if soup.css_first('link[rel="canonical"]'):
            selectors['link'] = 'link[rel="canonical"]'
        elif soup.css_first('meta[property="og:url"]'):
            selectors['link'] = 'meta[property="og:url"]'

        if soup.css_first('meta[property="product:brand"]'):
            selectors['brand_selector'] = 'meta[property="product:brand"]'
        elif soup.css_first('[itemprop="brand"]'):
            selectors['brand_selector'] = '[itemprop="brand"]'
        elif soup.css_first('[class*="brand"], [id*="brand"]'):
            selectors['brand_selector'] = '[class*="brand"], [id*="brand"]'

        return selectors
        

    def parse_soup_with_llm(self, soup: HTMLParser):
        """Extract the data with llm and save to db"""
        
        return {}

    def parse(self, html: str) -> dict:
        """Parse html to dictionnary"""
        soup = HTMLParser(html)
        result=self.parse_soup_with_meta(soup)
        k=len(result)
        if k!=5:
            print("Meta insuffisant, on passe à LLM")
        
        llm_results = self.parse_soup_with_llm(soup)
        result.update(llm_results) 
        return result

    def extract_data(self, html: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extrait les données du HTML en utilisant les sélecteurs fournis."""
        soup = HTMLParser(html)
        data = {}
        for key, selector in selectors.items():
            
            if 'selector' not in key and key != 'link':
                continue 

            if not selector:
                continue

            clean_key = key.replace('_selector', '')
            
            element = soup.css_first(selector)
            if element:
                if element.tag in ['meta', 'link']:
                    data[clean_key] = element.attributes.get('content') or element.attributes.get('href')
                else:
                    data[clean_key] = element.text(strip=True)
            else:
                data[clean_key] = None
        return data