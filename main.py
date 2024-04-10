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

@app.get("/logs")
async def get_all():
    cursor.execute("SELECT * FROM logs")
    result = cursor.fetchall()
    logs = []
    for row in result:
        log = {
            "timestamp": row[0],
            "http_method": row[1],
            "url": row[2],
            "user_agent": row[3],
            "client_ip": row[4]
        }
        logs.append(log)
    return {"logs": logs}

@app.get("/logs/{method}")
async def get_method(method: str):
    cursor.execute("SELECT * FROM logs WHERE http_method = %s", (method,))
    result = cursor.fetchall()
    logs = []
    for row in result:
        log = {
            "timestamp": row[0],
            "http_method": row[1],
            "url": row[2],
            "user_agent": row[3],
            "client_ip": row[4]
        }
        logs.append(log)
    return {"logs": logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
