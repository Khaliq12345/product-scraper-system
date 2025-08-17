import uvicorn
from src.api import app


def main():
    print("Hello from product-scraper-system!")
    uvicorn.run(app.app)


if __name__ == "__main__":
    main()
