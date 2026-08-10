MATCH (p:Person)
WHERE p.id = $personId
MATCH (p)-[:HAS_SKILL]->(s:Skill)
MATCH (j:JobRole)-[:REQUIRES]->(s)
MATCH (j)-[:USES]->(t:Technology)
RETURN p.name AS person, j.name AS jobRole, collect(DISTINCT s.name) AS sharedSkills, collect(DISTINCT t.name) AS technologies
ORDER BY j.name
