from src.core.requests_scraper import StaticScraper

if __name__ == "__main__":
    urll="https://www.asos.com/us/nike/nike-shox-r4-sneakers-in-black-and-silver/prd/207494721#colourWayId-207494724"
    print("Lancement du scraping pour ",urll)
    scraper = StaticScraper(url=urll)
    scraper.run()
    
    print("Scraping terminé.")


