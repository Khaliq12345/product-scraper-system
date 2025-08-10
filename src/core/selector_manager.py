from selectolax.parser import HTMLParser
from typing import Dict,Optional

class SelectorManager:
    def __init__(self) -> None:
        pass

    def parse_soup_with_meta(self, soup: HTMLParser)-> Dict[str,Optional[str]]:

        """Extract the data with popular metadata and save to db"""
        selectors = {}
        if soup.css_first('title'):
              selectors['selector_title'] = 'title'
        elif soup.css_first('meta[property="og:title"]'):
            selectors['selector_title'] = 'meta[property="og:title"]'
        
        if soup.css_first('meta[property="product:price:amount"]'):
            selectors['selector_price'] = 'meta[property="product:price:amount"]'
        elif soup.css_first('meta[itemprop="price"]'):
            selectors['selector_price'] = 'meta[itemprop="price"]'
        elif soup.css_first('[class*="price"], [id*="price"]'):
            selectors['selector_price'] = '[class*="price"], [id*="price"]'

        if soup.css_first('meta[property="og:image"]'):
            selectors['selector_image'] = 'meta[property="og:image"]'
        elif soup.css_first('img[itemprop="image"]'):
            selectors['selector_image'] = 'img[itemprop="image"]'
        elif soup.css_first('img[class*="product-image"], img[id*="product-image"]'):
            selectors['selector_image'] = 'img[class*="product-image"], img[id*="product-image"]'
        
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
        
        pass

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
