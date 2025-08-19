from fastapi import FastAPI, BackgroundTasks
from src.core.orchestrator import Orchestrator
from src.core.database_manager import DataManager
from time import time

app = FastAPI(title="Product Scraper")


@app.get("/api/scrape-product")
def scrape_product(background_tasks: BackgroundTasks, url: str):
    product_id = int(time())
    product_id = f"product_{product_id}"
    runner = Orchestrator(url, product_id)
    background_tasks.add_task(runner.main)
    return {"details": {"product_id": product_id}}


@app.get("/api/get-product")
def get_product(product_id: str):
    db_manager = DataManager()
    product = db_manager.get_product_info(product_id)
    return {"details": product}
