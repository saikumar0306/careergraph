MATCH (j:JobRole)
WHERE j.id = $jobRoleId
MATCH (j)-[:REQUIRES]->(s:Skill)
RETURN s.id AS id, s.name AS name, s.category AS category
ORDER BY s.name
