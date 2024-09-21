import requests
from fastapi import Depends, FastAPI, HTTPException, Response, Request
from sqlalchemy.orm import Session
from typing import List
import os
import crud_utils
import models
import schemas
import parser_prices
from database import SessionLocal, engine
from background_task import periodic
import asyncio
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from rocketry import Rocketry

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

app_rocketry = Rocketry(execution="async")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

root = os.path.dirname(os.path.abspath(__file__))

#app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app_rocketry.task("every 10 seconds")
# async def do_things():
#     db = Depends(get_db)
#     products = parser_prices.start_parser()
#     for product in products:
#         json_data = {
#             'name': product["name"],
#             'price': product["price"],
#         }
#         crud_utils.create_product(db, product)
#         response = requests.post('http://127.0.0.1:8000/product/', headers=headers, json=json_data)


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic())


# @app.get("/item/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return id


@app.post("/product/") #, response_model=schemas.ProductCreate
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    product_exists = crud_utils.get_product_by_name(db, name=product.name)
    if not product_exists or product_exists.price != product.price:
        return crud_utils.create_product(db=db, product=product)


@app.get("/products/") #, response_model=List[schemas.Product]
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud_utils.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/product/{product_id}") #, response_model=schemas.Product
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_utils.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product with id=\'{product_id}\' not found")
    return db_product


@app.get("/product/get-product-by-name/{product_name}") #, response_model=schemas.Product
def read_product_by_name(product_name: str, db: Session = Depends(get_db)):
    db_product = crud_utils.get_product_by_name(db, name=product_name)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product with name=\'{product_name}\' not found")
    return db_product


@app.put("/product/{product_id}") #, response_model=schemas.Product
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud_utils.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product with id=\'{product_id}\' not found")
    return crud_utils.update_product(db, product=product, product_id=product_id)


@app.delete("/product/{product_id}") #, response_model=dict
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_utils.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product with id=\'{product_id}\' not found")
    crud_utils.delete_product(db, product_id=product_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
