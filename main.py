from fastapi import FastAPI, Request, Response
from datetime import datetime
from pymongo import MongoClient
from bson import json_util
import json

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
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
async def read_root():
    return {"message": "Olá, mundo!"}

@app.get("/logs")
async def get_all():
    logs = list(collection.find({}))
    for log in logs:
        log['_id'] = str(log['_id'])
    return {"logs": logs}

@app.get("/logs/{method}")
async def get_method(method: str):
    logs = list(collection.find({"http_method": method.upper()}))
    for log in logs:
        log['_id'] = str(log['_id'])
    return {"logs": logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
