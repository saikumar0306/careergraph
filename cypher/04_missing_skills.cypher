MATCH (p:Person)
WHERE p.id = $personId
MATCH (j:JobRole)
WHERE j.id = $jobRoleId
MATCH (j)-[:REQUIRES]->(required:Skill)
OPTIONAL MATCH (p)-[:HAS_SKILL]->(owned:Skill)
WHERE owned.id = required.id
WITH required, owned
WHERE owned IS NULL
RETURN required.id AS id, required.name AS name, required.category AS category
ORDER BY required.name
