import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", ".env"))


def get_db_connection():
    uri = os.getenv("COGNODB_URI", "").strip()
    username = os.getenv("COGNODB_USERNAME", "").strip()
    password = os.getenv("COGNODB_PASSWORD", "").strip()

    if not uri or not username or not password:
        raise ValueError("Missing CognoDB environment variables")

    return GraphDatabase.driver(uri, auth=(username, password))


def check_db_connection():
    driver = get_db_connection()
    try:
        driver.verify_connectivity()
        return True
    finally:
        driver.close()
