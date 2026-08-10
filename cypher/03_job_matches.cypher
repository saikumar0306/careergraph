MATCH (p:Person)
WHERE p.id = $personId
MATCH (p)-[:HAS_SKILL]->(s:Skill)
MATCH (j:JobRole)-[:REQUIRES]->(s)
RETURN DISTINCT j.id AS id, j.name AS name, j.description AS description
ORDER BY j.name
