from __future__ import annotations
from typing import Union
from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    datetime: datetime
