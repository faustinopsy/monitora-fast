from fastapi import FastAPI, Request
from datetime import datetime
from rethinkdb import RethinkDB
r = RethinkDB()

app = FastAPI()


conn = r.connect("localhost", 28015)

db_name = "test"
table_name = "teste"

def insert_log(log_data):
    r.db(db_name).table(table_name).insert(log_data).run(conn)

@app.middleware("http")
async def log_request(request: Request, call_next):
    user_agent = request.headers.get('user-agent')
    client_ip = request.client.host
    http_method = request.method
    url = request.url.path

    timestamp = r.now()

    log_data = {
        "timestamp": timestamp,
        "http_method": http_method,
        "url": url,
        "user_agent": user_agent,
        "client_ip": client_ip
    }
    insert_log(log_data)

    response = await call_next(request)
    return response

@app.get("/logs")
async def get_all():
    logs = list(r.db(db_name).table(table_name).run(conn))
    return {"logs": logs}

@app.get("/logs/{method}")
async def get_method(method: str):
    logs = list(r.db(db_name).table(table_name).filter({"http_method": method.upper()}).run(conn))
    return {"logs": logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
