from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.database.connection import check_db_connection

app = FastAPI(title="CareerGraph API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "CareerGraph API is running", "status": "ok"}


@app.get("/health/db")
def health_db():
    try:
        if check_db_connection():
            return {"database": "connected", "status": "ok"}
    except Exception:
        pass

    return JSONResponse(status_code=503, content={"database": "unavailable", "status": "error"})
