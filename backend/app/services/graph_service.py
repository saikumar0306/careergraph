from __future__ import annotations

from typing import Any

from neo4j.exceptions import AuthError, Neo4jError, ServiceUnavailable

try:
    from backend.database.connection import get_db_connection
except ModuleNotFoundError:  # pragma: no cover - supports running app from backend directory
    from database.connection import get_db_connection


class GraphServiceError(Exception):
    pass


class NotFoundError(GraphServiceError):
    pass


class DatabaseUnavailableError(GraphServiceError):
    pass


def _run_query(query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    driver = get_db_connection()
    try:
        with driver.session() as session:
            result = list(session.run(query, params or {}))
            return [dict(record) for record in result]
    except ServiceUnavailable as exc:
        raise DatabaseUnavailableError("Database unavailable") from exc
    except (AuthError, Neo4jError) as exc:
        raise DatabaseUnavailableError("Database unavailable") from exc
    except ValueError as exc:
        raise DatabaseUnavailableError("Database unavailable") from exc
    finally:
        driver.close()


def list_jobs() -> list[dict[str, Any]]:
    query = """
    MATCH (j:JobRole)
    RETURN j.id AS id, j.name AS name, j.description AS description
    ORDER BY j.name
    """
    return _run_query(query)


def get_job(job_id: str) -> dict[str, Any]:
    query = """
    MATCH (j:JobRole {id: $job_id})
    RETURN j.id AS id, j.name AS name, j.description AS description
    """
    records = _run_query(query, {"job_id": job_id})
    if not records:
        raise NotFoundError("Job not found")
    return records[0]


def get_job_skills(job_id: str) -> dict[str, Any]:
    job = get_job(job_id)
    query = """
    MATCH (j:JobRole {id: $job_id})-[:REQUIRES]->(s:Skill)
    RETURN s.id AS id, s.name AS name
    ORDER BY s.name
    """
    skills = _run_query(query, {"job_id": job_id})
    return {"job": job["name"], "skills": skills}


def list_people() -> list[dict[str, Any]]:
    query = """
    MATCH (p:Person)
    RETURN p.id AS id, p.name AS name, p.title AS title
    ORDER BY p.name
    """
    return _run_query(query)


def get_person_name(person_id: str) -> str:
    query = """
    MATCH (p:Person {id: $person_id})
    RETURN p.name AS name
    """
    person_records = _run_query(query, {"person_id": person_id})
    if not person_records:
        raise NotFoundError("Person not found")
    return person_records[0]["name"]


def get_person_matches(person_id: str) -> list[dict[str, Any]]:
    get_person_name(person_id)

    query = """
    MATCH (p:Person {id: $person_id})-[:HAS_SKILL]->(s:Skill)
    MATCH (j:JobRole)-[:REQUIRES]->(s)
    WITH j, collect(DISTINCT s) AS sharedSkills
    MATCH (j)-[:REQUIRES]->(required:Skill)
    WITH j, sharedSkills, size(sharedSkills) AS matchingSkillCount, count(DISTINCT required) AS requiredSkillCount
    RETURN j.id AS id,
           j.name AS name,
           matchingSkillCount AS matching_skills,
           CASE
               WHEN requiredSkillCount > 0 THEN toFloat(matchingSkillCount) / toFloat(requiredSkillCount) * 100.0
               ELSE 0.0
           END AS match_percentage
    ORDER BY match_percentage DESC, j.name
    """
    return _run_query(query, {"person_id": person_id})


def get_missing_skills(person_id: str, job_id: str) -> dict[str, Any]:
    person_name = get_person_name(person_id)

    job = get_job(job_id)
    query = """
    MATCH (p:Person {id: $person_id})
    MATCH (j:JobRole {id: $job_id})
    MATCH (j)-[:REQUIRES]->(required:Skill)
    OPTIONAL MATCH (p)-[:HAS_SKILL]->(owned:Skill)
    WHERE owned.id = required.id
    WITH required, owned
    WHERE owned IS NULL
    RETURN required.name AS name
    ORDER BY required.name
    """
    missing_skills = _run_query(query, {"person_id": person_id, "job_id": job_id})
    return {
        "person": person_name,
        "job": job["name"],
        "missing_skills": [skill["name"] for skill in missing_skills],
    }


def get_skill_connections(skill_id: str) -> dict[str, Any]:
    skill_query = """
    MATCH (s:Skill {id: $skill_id})
    RETURN s.id AS id, s.name AS name
    """
    skill_records = _run_query(skill_query, {"skill_id": skill_id})
    if not skill_records:
        raise NotFoundError("Skill not found")

    job_query = """
    MATCH (s:Skill {id: $skill_id})
    OPTIONAL MATCH (j:JobRole)-[:REQUIRES]->(s)
    RETURN collect(DISTINCT {id: j.id, name: j.name}) AS job_roles
    """
    technology_query = """
    MATCH (s:Skill {id: $skill_id})
    OPTIONAL MATCH (j:JobRole)-[:REQUIRES]->(s)
    OPTIONAL MATCH (j)-[:USES]->(t:Technology)
    RETURN collect(DISTINCT {id: t.id, name: t.name}) AS technologies
    """

    job_roles = _run_query(job_query, {"skill_id": skill_id})
    technologies = _run_query(technology_query, {"skill_id": skill_id})

    return {
        "skill": skill_records[0]["name"],
        "job_roles": [job for job in job_roles[0]["job_roles"] if job["id"] is not None],
        "technologies": [tech for tech in technologies[0]["technologies"] if tech["id"] is not None],
    }
