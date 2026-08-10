import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

uri = os.getenv('COGNODB_URI', '')
user = os.getenv('COGNODB_USERNAME', '')
pwd = os.getenv('COGNODB_PASSWORD', '')

driver = GraphDatabase.driver(uri, auth=(user, pwd))

with driver.session() as session:
    node_counts = list(session.run('MATCH (n) RETURN labels(n) AS labels, count(*) AS count ORDER BY count DESC'))
    rel_counts = list(session.run('MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count ORDER BY count DESC'))
    print(node_counts)
    print(rel_counts)

driver.close()
