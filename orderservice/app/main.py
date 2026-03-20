import os
import requests
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Order Service")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)

Base.metadata.create_all(engine)

@app.post("/order")
def place(user_id: int, product_id: int):
    db = SessionLocal()
    db.add(Order(user_id=user_id, product_id=product_id))
    db.commit()
    return {"message": "Order placed"}

@app.get("/health")
def health():
    return {"status": "ok"}
