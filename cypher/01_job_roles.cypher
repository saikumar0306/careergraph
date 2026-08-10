MATCH (j:JobRole)
RETURN j.id AS id, j.name AS name, j.description AS description
ORDER BY j.name
