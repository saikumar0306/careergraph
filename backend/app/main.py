from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.database.connection import check_db_connection
from app.routes.graph_routes import router as graph_router

app = FastAPI(title="CareerGraph API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graph_router)


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
