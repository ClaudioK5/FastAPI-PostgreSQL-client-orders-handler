from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship("Order", back_populates="customer")

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key= True, index=True)

    product_name= Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    price = Column(Float, nullable=True)

    customer = relationship("Customer", back_populates="orders")
