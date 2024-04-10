from fastapi import FastAPI, Request
from datetime import datetime
from pymongo import MongoClient

app = FastAPI()

client = MongoClient('localhost', 27017)
db = client['logs_database']
collection = db['logs_collection']

@app.middleware("http")
async def log_request(request: Request, call_next):
    user_agent = request.headers.get('user-agent')
    client_ip = request.client.host
    http_method = request.method
    url = request.url.path
    timestamp = datetime.now()

    log_data = {
        "timestamp": timestamp,
        "http_method": http_method,
        "url": url,
        "user_agent": user_agent,
        "client_ip": client_ip
    }
    collection.insert_one(log_data)

    response = await call_next(request)
    return response

@app.get("/")
async def inicio():
    return {"message": "Olá, mundo!"}

@app.post("/item")
async def examplo_post():
    return {"message": "Exemplo de POST"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
