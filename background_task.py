import asyncio
from sqlalchemy.orm import Session
from datetime import datetime
import models
from fastapi import Depends
from database import SessionLocal
from parser_prices import start_parser
import schemas
import main
from fastapi.responses import JSONResponse, FileResponse
import requests

import crud_utils

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def periodic():
    while True:
        print("Background worker started at ", datetime.now())
        products = start_parser()
        db = SessionLocal()

        def send_data_task():
            for product in products:
                json_data = {
                    'name': product["name"],
                    'price': product["price"],
                }
                response = requests.post('http://127.0.0.1:8000/product/', headers=headers, json=json_data)
                #item = schemas.ProductCreate(name=product['name'], price=product['price'])
                #crud_utils.create_product(db=db, product=item)
                #main.create_product(product=item)

        loop = asyncio.get_running_loop()
        awaitable = loop.run_in_executor(None, send_data_task)
        await asyncio.sleep(1000)
