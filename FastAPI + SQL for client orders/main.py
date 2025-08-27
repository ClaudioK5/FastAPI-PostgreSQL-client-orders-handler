from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from email_sender import send_email
from database import SessionLocal, engine, Base
from sqlalchemy import extract
Base.metadata.create_all(bind=engine)
from datetime import datetime
from openai import OpenAI


client = OpenAI(
    api_key="insert your deepseek api key here",
    base_url="https://api.deepseek.com/v1"
)


app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):

    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):

    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()

    if not customer:

        raise HTTPException(status_code=404, detail="Customer not found")

    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Order).offset(skip).limit(limit).all()

@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Customer).offset(skip).limit(limit).all()

@app.get("/generate_report")
def generate_report(db: Session = Depends(get_db)):

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    orders = db.query(models.Order).filter(extract('year', models.Order.timestamp) == current_year, extract('month', models.Order.timestamp) == current_month).all()
    print(orders)
    if not orders:

        return {'message': "no orders found for the current month"}

    orders_summary = ""

    for order in orders:

        orders_summary +=f"""Customer ID: {order.customer_id} Product: {order.product_name} Quantity: {order.amount} Data: {order.timestamp.strftime('%Y-%m-%d')}\n"""

    print(orders_summary)

    prompt ="""Analyze the following orders in the current month and make a general overview of the most selled items,
     anomalies, and eventual suggestions to improve sales:\n\n"""+ orders_summary + """\n\nRemember that each Customer ID represent a singular individual that made the order.
      So in case you see Customer 1 two or more times, it is still referred to the same Customer. 
      DO NOT MAKE any calculation, only a short overview ideally with bulletpoints is needed."""


    print(prompt)
    try:
        response = client.chat.completions.create(model="deepseek-chat",
                                                      messages=[{'role': 'user', 'content': prompt}],
                                                      max_tokens=300)

        ai_output = response.choices[0].message.content.strip()

        print(ai_output)

        subject = 'AI report for the current month'

        send_email('insert your email here', subject, ai_output)

        print("email sent successfully!")

    except Exception as e:

       return {"error": str(e)}

    return ai_output


