import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

uri = os.getenv('COGNODB_URI', '')
user = os.getenv('COGNODB_USERNAME', '')
pwd = os.getenv('COGNODB_PASSWORD', '')

driver = GraphDatabase.driver(uri, auth=(user, pwd))
query = 'MATCH (j:JobRole) WHERE j.id = $jobRoleId MATCH (j)-[:REQUIRES]->(s:Skill) RETURN s.id AS id, s.name AS name, s.category AS category ORDER BY s.name'
with driver.session() as session:
    result = list(session.run(query, jobRoleId='jobrole:data-scientist'))
    print(result)
driver.close()
