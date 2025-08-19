import uvicorn
from src.api import app
from src.config.config import ENV


def main():
    print("Hello from product-scraper-system!")
    uvicorn.run("src.api.app:app", host="0.0.0.0", reload=ENV == "dev")


if __name__ == "__main__":
    main()
