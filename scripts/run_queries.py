import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

uri = os.getenv('COGNODB_URI', '')
user = os.getenv('COGNODB_USERNAME', '')
pwd = os.getenv('COGNODB_PASSWORD', '')

driver = GraphDatabase.driver(uri, auth=(user, pwd))

queries = [
    ('01_job_roles', 'MATCH (j:JobRole) RETURN j.id AS id, j.name AS name, j.description AS description ORDER BY j.name'),
    ('02_job_skills', 'MATCH (j:JobRole) WHERE j.id = $jobRoleId MATCH (j)-[:REQUIRES]->(s:Skill) RETURN s.id AS id, s.name AS name, s.category AS category ORDER BY s.name'),
    ('03_job_matches', 'MATCH (p:Person) WHERE p.id = $personId MATCH (p)-[:HAS_SKILL]->(s:Skill) MATCH (j:JobRole)-[:REQUIRES]->(s) RETURN DISTINCT j.id AS id, j.name AS name, j.description AS description ORDER BY j.name'),
    ('04_missing_skills', 'MATCH (p:Person) WHERE p.id = $personId MATCH (j:JobRole) WHERE j.id = $jobRoleId MATCH (j)-[:REQUIRES]->(required:Skill) OPTIONAL MATCH (p)-[:HAS_SKILL]->(owned:Skill) WHERE owned.id = required.id WITH required, owned WHERE owned IS NULL RETURN required.id AS id, required.name AS name, required.category AS category ORDER BY required.name'),
    ('05_multi_hop', 'MATCH (p:Person) WHERE p.id = $personId MATCH (p)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(j:JobRole)-[:USES]->(t:Technology) RETURN p.name AS person, s.name AS skill, j.name AS jobRole, t.name AS technology ORDER BY j.name, t.name'),
    ('06_graph_exploration', 'MATCH (p:Person) WHERE p.id = $personId MATCH (p)-[:HAS_SKILL]->(s:Skill) MATCH (j:JobRole)-[:REQUIRES]->(s) MATCH (j)-[:USES]->(t:Technology) RETURN p.name AS person, j.name AS jobRole, collect(DISTINCT s.name) AS sharedSkills, collect(DISTINCT t.name) AS technologies ORDER BY j.name'),
]

with driver.session() as session:
    params = {'jobRoleId': 'jobrole:data-scientist', 'personId': 'person:maya'}
    for name, query in queries:
        result = list(session.run(query, params))
        print(f'{name}: {len(result)} rows')
        for record in result[:3]:
            print(record)
        print('---')

driver.close()
