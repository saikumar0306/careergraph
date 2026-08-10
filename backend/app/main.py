from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from backend.database.connection import check_db_connection, get_env_presence
    from backend.app.routes.graph_routes import router as graph_router
except ModuleNotFoundError:  # pragma: no cover - supports running app from backend directory
    from database.connection import check_db_connection, get_env_presence
    from app.routes.graph_routes import router as graph_router

app = FastAPI(title="CareerGraph API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://careergraph-yn92.onrender.com",
    ],
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
    env_presence = get_env_presence()
    try:
        if check_db_connection():
            return {"database": "connected", "status": "ok", "env_present": env_presence}
    except Exception:
        pass

    return JSONResponse(
        status_code=503,
        content={"database": "unavailable", "status": "error", "env_present": env_presence},
    )
