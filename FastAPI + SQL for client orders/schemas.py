from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class OrderCreate(BaseModel):

    product_name: str
    amount: float
    customer_id: int


class Order(BaseModel):

    id: int
    product_name: str
    amount: float
    timestamp: datetime
    customer_id: int

    class Config:

        orm_mode = True

class CustomerCreate(BaseModel):

    name: str
    email: str

class Customer(BaseModel):

    id: int
    name: str
    email: str
    orders: List[Order] = []

    class Config:

        orm_mode = True