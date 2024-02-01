from pydantic import BaseModel
from typing import List
from bson import ObjectId


class Address(BaseModel):
    city: str
    country: str
    zip_code: str


class OrderItem(BaseModel):
    product_id: str
    bought_quantity: int


class CreateOrderRequest(BaseModel):
    items: List[OrderItem]
    user_address: Address

    class Config:
        arbitrary_types_allowed = True