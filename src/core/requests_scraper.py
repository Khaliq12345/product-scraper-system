
import hrequests

class HTTPManager:
  
    def __init__(self):
        
        self.session = hrequests.Session(
            browser='chrome',  
            os='win'
        )
       
    def fetch_html(self, url: str) -> str | None:
        
        try:
           
            response = self.session.get(url, timeout=20)
            
           
            if response.status_code == 200:
               
                return response.text
            else:
                print(f"Erreur de statut de la requête : {response.status_code}")
                return None
            
        except Exception as e:
            
            print(f"Une erreur est survenue lors de la requête hrequests vers {url}: {e}")
            return None