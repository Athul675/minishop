import requests
from fastapi import FastAPI, Request

app = FastAPI(title="API Gateway")

@app.api_route("/api/{service}/{path:path}", methods=["GET","POST"])
async def proxy(service: str, path: str, request: Request):

    url = f"http://{service}:8000/{path}"
    body = await request.body()

    response = requests.request(
        request.method,
        url,
        data=body,
        headers={"Content-Type":"application/json"}
    )

    return response.json()

@app.get("/health")
def health():
    return {"status": "ok"}
