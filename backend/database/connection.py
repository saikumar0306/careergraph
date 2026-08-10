import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


def _load_dotenv():
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parents[1] / ".env",
        Path(__file__).resolve().parents[2] / ".env",
    ]

    for dotenv_path in candidates:
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)
            break


_load_dotenv()


def get_db_connection():
    uri = os.getenv("COGNODB_URI", "").strip()
    username = os.getenv("COGNODB_USERNAME", "").strip()
    password = os.getenv("COGNODB_PASSWORD", "").strip()

    if not uri or not username or not password:
        raise ValueError("Missing CognoDB environment variables")

    return GraphDatabase.driver(uri, auth=(username, password))


def get_env_presence() -> dict[str, bool]:
    return {
        "COGNODB_URI": bool(os.getenv("COGNODB_URI", "").strip()),
        "COGNODB_USERNAME": bool(os.getenv("COGNODB_USERNAME", "").strip()),
        "COGNODB_PASSWORD": bool(os.getenv("COGNODB_PASSWORD", "").strip()),
    }


def check_db_connection():
    driver = get_db_connection()
    try:
        driver.verify_connectivity()
        return True
    finally:
        driver.close()
