from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas
from fastapi import HTTPException
# from . import models, schemas


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def get_products_by_datetime(db: Session, date: str):
    return db.query(models.Product).filter(models.Product.datetime == date).all()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).all()


def create_product(db: Session, product: schemas.ProductCreate):
    if product.price == 0:
        return

    db_product = models.Product(
        name=product.name,
        price=product.price,
        datetime=datetime.now())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product: schemas.ProductUpdate, product_id: int):
    db_product = get_product_by_id(db, product_id=product_id)
    product_data = product.dict()

    for key, value in product_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    db.commit()
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id=product_id)

    db.delete(db_product)
    db.commit()
