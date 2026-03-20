import os
import redis
from fastapi import FastAPI
 
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
 
r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    password=REDIS_PASSWORD,
    decode_responses=True
)
 
app = FastAPI(title="Cart Service")
 
@app.post("/cart/{user_id}/add/{product_id}")
def add(user_id: str, product_id: str):
    r.rpush(user_id, product_id)
    return {"message": "Added"}
 
@app.get("/cart/{user_id}")
def get(user_id: str):
    return r.lrange(user_id, 0, -1)
 
@app.get("/health")
def health():
    return {"status": "ok"}
