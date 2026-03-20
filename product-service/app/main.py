import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", 10))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Product Service")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

Base.metadata.create_all(engine)

class ProductSchema(BaseModel):
    name: str
    price: float

@app.post("/products")
def create_product(product: ProductSchema):
    db = SessionLocal()
    db.add(Product(name=product.name, price=product.price))
    db.commit()
    return {"message": "Created"}

@app.get("/products")
def list_products():
    db = SessionLocal()
    return db.query(Product).limit(PAGE_SIZE).all()

@app.get("/health")
def health():
    return {"status": "ok"}
