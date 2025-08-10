import pytest
from selectolax.parser import HTMLParser
from src.core.selector_manager import SelectorManager  # adapte selon où tu ranges ta classe

def test_parse_soup_with_meta_title_only():
    html = "<html><head><title>Mon super produit</title></head><body></body></html>"
    soup = HTMLParser(html)
    manager = SelectorManager()
    selectors = manager.parse_soup_with_meta(soup)

    assert 'selector_title' in selectors
    assert selectors['selector_title'] == 'title'
    assert 'selector_price' not in selectors
    assert 'selector_image' not in selectors
    assert 'link' not in selectors
    assert 'brand_selector' not in selectors

def test_parse_soup_with_meta_full():
    html = """
    <html>
    <head>
        <title>Produit Test</title>
        <meta property="og:title" content="Produit Test OG">
        <meta property="product:price:amount" content="123.45">
        <meta property="og:image" content="image.jpg">
        <link rel="canonical" href="https://example.com/produit-test">
        <meta property="product:brand" content="MaMarque">
    </head>
    <body></body>
    </html>
    """
    soup = HTMLParser(html)
    manager = SelectorManager()
    selectors = manager.parse_soup_with_meta(soup)

    assert selectors['selector_title'] == 'title'
    assert selectors['selector_price'] == 'meta[property="product:price:amount"]'
    assert selectors['selector_image'] == 'meta[property="og:image"]'
    assert selectors['link'] == 'link[rel="canonical"]'
    assert selectors['brand_selector'] == 'meta[property="product:brand"]'

def test_parse_method_calls_meta_and_llm(monkeypatch):
    html = "<html><head><title>Titre</title></head></html>"
    manager = SelectorManager()

    monkeypatch.setattr(manager, "parse_soup_with_llm", lambda soup: {"llm": "result"})

    result = manager.parse(html)

    assert 'selector_title' in result
    assert 'llm' in result
