from fastapi import FastAPI, Request
import mysql.connector
from datetime import datetime

app = FastAPI()

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'log_fast'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.on_event("shutdown")
def shutdown_event():
    conn.close()

@app.middleware("http")
async def log_request(request: Request, call_next):
    user_agent = request.headers.get('user-agent')
    client_ip = request.client.host
    http_method = request.method
    url = request.url.path
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = "INSERT INTO logs (data, http_method, url, user_agent, client_ip) VALUES (%s, %s, %s, %s, %s)"
    values = (timestamp, http_method, url, user_agent, client_ip)
    cursor.execute(sql, values)
    conn.commit()

    response = await call_next(request)
    return response

@app.get("/")
async def read_root():
    return {"message": "Olá, mundo!"}

@app.post("/item")
async def example_post():
    return {"message": "Exemplo de POST"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
