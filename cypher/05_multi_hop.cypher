MATCH (p:Person)
WHERE p.id = $personId
MATCH (p)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(j:JobRole)-[:USES]->(t:Technology)
RETURN p.name AS person, s.name AS skill, j.name AS jobRole, t.name AS technology
ORDER BY j.name, t.name
