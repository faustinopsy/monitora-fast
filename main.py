from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime

app = FastAPI()

log = "log.txt"

@app.middleware("http")
async def log_request(request: Request, call_next):
    user_agent = request.headers.get('user-agent')
    client_ip = request.client.host
    http_method = request.method
    url = request.url.path

    with open(log, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escreva_log = f"{timestamp} - HTTP Method: {http_method} | URL: {url} | User-Agent: {user_agent} | Client IP: {client_ip}\n"
        file.write(escreva_log)

    response = await call_next(request)

    return response

@app.get("/")
async def inicio():
    return {"message": "Olá, mundo!"}

@app.post("/item")
async def examplo_post():
    return {"message": "Exemplo de POST"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
