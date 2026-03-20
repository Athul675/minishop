import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.hash import bcrypt
from jose import jwt
from pydantic import BaseModel

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="User Service")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(engine)

class UserSchema(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(user: UserSchema):
    db = SessionLocal()
    hashed = bcrypt.hash(user.password)
    db.add(User(email=user.email, password=hashed))
    db.commit()
    return {"message": "User registered"}

@app.post("/login")
def login(user: UserSchema):
    db = SessionLocal()
    db_user = db.query(User).filter_by(email=user.email).first()

    if not db_user or not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"email": user.email}, JWT_SECRET, algorithm="HS256")
    return {"token": token}

@app.get("/health")
def health():
    return {"status": "ok"}
