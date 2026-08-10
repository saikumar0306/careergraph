import os
from typing import Any

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

URI = os.getenv("COGNODB_URI", "").strip()
USERNAME = os.getenv("COGNODB_USERNAME", "").strip()
PASSWORD = os.getenv("COGNODB_PASSWORD", "").strip()

if not URI or not USERNAME or not PASSWORD:
    raise RuntimeError("Missing CognoDB environment variables")


def run_query(tx: Any, query: str, parameters: dict[str, Any] | None = None) -> None:
    tx.run(query, parameters or {})


def create_graph() -> None:
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    try:
        with driver.session() as session:
            session.execute_write(run_query, "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE")
            session.execute_write(run_query, "CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE")
            session.execute_write(run_query, "CREATE CONSTRAINT jobrole_id IF NOT EXISTS FOR (j:JobRole) REQUIRE j.id IS UNIQUE")
            session.execute_write(run_query, "CREATE CONSTRAINT technology_id IF NOT EXISTS FOR (t:Technology) REQUIRE t.id IS UNIQUE")
            session.execute_write(run_query, "CREATE CONSTRAINT project_id IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE")
            session.execute_write(run_query, "CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE")

            session.execute_write(run_query, """
                UNWIND $people AS person
                MERGE (p:Person {id: person.id})
                SET p.name = person.name,
                    p.title = person.title
            """, {"people": [
                {"id": "person:ana", "name": "Ana Patel", "title": "Data Scientist"},
                {"id": "person:ben", "name": "Ben Carter", "title": "Machine Learning Engineer"},
                {"id": "person:chris", "name": "Chris Kim", "title": "Backend Engineer"},
                {"id": "person:dana", "name": "Dana Flores", "title": "Frontend Engineer"},
                {"id": "person:eli", "name": "Eli Brooks", "title": "DevOps Engineer"},
                {"id": "person:fiona", "name": "Fiona Chen", "title": "Product Analyst"},
                {"id": "person:greg", "name": "Greg Nguyen", "title": "Research Engineer"},
                {"id": "person:hina", "name": "Hina Shah", "title": "Data Engineer"},
                {"id": "person:ivy", "name": "Ivy Gomez", "title": "Software Engineer"},
                {"id": "person:jo", "name": "Jo Alvarez", "title": "AI Engineer"},
                {"id": "person:maya", "name": "Maya Singh", "title": "Data Analyst"},
            ]})

            session.execute_write(run_query, """
                UNWIND $skills AS skill
                MERGE (s:Skill {id: skill.id})
                SET s.name = skill.name,
                    s.category = skill.category
            """, {"skills": [
                {"id": "skill:python", "name": "Python", "category": "Programming"},
                {"id": "skill:sql", "name": "SQL", "category": "Data"},
                {"id": "skill:ml", "name": "Machine Learning", "category": "AI"},
                {"id": "skill:statistics", "name": "Statistics", "category": "Data"},
                {"id": "skill:react", "name": "React", "category": "Frontend"},
                {"id": "skill:fastapi", "name": "FastAPI", "category": "Backend"},
                {"id": "skill:docker", "name": "Docker", "category": "DevOps"},
                {"id": "skill:kubernetes", "name": "Kubernetes", "category": "DevOps"},
                {"id": "skill:pytorch", "name": "PyTorch", "category": "AI"},
                {"id": "skill:aws", "name": "AWS", "category": "Cloud"},
                {"id": "skill:neo4j", "name": "Neo4j", "category": "Database"},
                {"id": "skill:cypher", "name": "Cypher", "category": "Database"},
                {"id": "skill:testing", "name": "Testing", "category": "Quality"},
                {"id": "skill:typescript", "name": "TypeScript", "category": "Programming"},
                {"id": "skill:git", "name": "Git", "category": "Tooling"},
                {"id": "skill:airflow", "name": "Airflow", "category": "Data"},
                {"id": "skill:tableau", "name": "Tableau", "category": "Data"},
                {"id": "skill:redis", "name": "Redis", "category": "Backend"},
                {"id": "skill:prometheus", "name": "Prometheus", "category": "Monitoring"},
                {"id": "skill:analytics", "name": "Analytics", "category": "Data"},
                {"id": "skill:linux", "name": "Linux", "category": "System"},
                {"id": "skill:pandas", "name": "Pandas", "category": "Data"},
            ]})

            session.execute_write(run_query, """
                UNWIND $job_roles AS job_role
                MERGE (j:JobRole {id: job_role.id})
                SET j.name = job_role.name,
                    j.description = job_role.description
            """, {"job_roles": [
                {"id": "jobrole:data-scientist", "name": "Data Scientist", "description": "Builds predictive models and analyzes data."},
                {"id": "jobrole:ml-engineer", "name": "Machine Learning Engineer", "description": "Deploys and maintains ML systems."},
                {"id": "jobrole:backend-engineer", "name": "Backend Engineer", "description": "Builds reliable API services."},
                {"id": "jobrole:frontend-engineer", "name": "Frontend Engineer", "description": "Creates polished user interfaces."},
                {"id": "jobrole:devops-engineer", "name": "DevOps Engineer", "description": "Keeps services reliable and deployed."},
                {"id": "jobrole:data-engineer", "name": "Data Engineer", "description": "Builds systems to move and model business data."},
                {"id": "jobrole:product-analyst", "name": "Product Analyst", "description": "Uses data to guide product decisions."},
                {"id": "jobrole:research-engineer", "name": "Research Engineer", "description": "Explores new technical approaches."},
                {"id": "jobrole:ai-engineer", "name": "AI Engineer", "description": "Builds products around AI capabilities."},
                {"id": "jobrole:software-engineer", "name": "Software Engineer", "description": "Builds and supports cross-functional software solutions."},
            ]})

            session.execute_write(run_query, """
                UNWIND $technologies AS technology
                MERGE (t:Technology {id: technology.id})
                SET t.name = technology.name,
                    t.category = technology.category
            """, {"technologies": [
                {"id": "tech:python", "name": "Python", "category": "Language"},
                {"id": "tech:react", "name": "React", "category": "Frontend"},
                {"id": "tech:fastapi", "name": "FastAPI", "category": "Backend"},
                {"id": "tech:pytorch", "name": "PyTorch", "category": "AI"},
                {"id": "tech:docker", "name": "Docker", "category": "DevOps"},
                {"id": "tech:kubernetes", "name": "Kubernetes", "category": "DevOps"},
                {"id": "tech:neo4j", "name": "Neo4j", "category": "Database"},
                {"id": "tech:aws", "name": "AWS", "category": "Cloud"},
                {"id": "tech:tableau", "name": "Tableau", "category": "Data"},
                {"id": "tech:redis", "name": "Redis", "category": "Cache"},
                {"id": "tech:airflow", "name": "Airflow", "category": "Data"},
                {"id": "tech:typescript", "name": "TypeScript", "category": "Language"},
                {"id": "tech:linux", "name": "Linux", "category": "System"},
                {"id": "tech:prometheus", "name": "Prometheus", "category": "Monitoring"},
                {"id": "tech:git", "name": "Git", "category": "Tooling"},
            ]})

            session.execute_write(run_query, """
                UNWIND $projects AS project
                MERGE (p:Project {id: project.id})
                SET p.name = project.name,
                    p.description = project.description
            """, {"projects": [
                {"id": "project:insight-platform", "name": "Insight Platform", "description": "A customer analytics platform for product teams."},
                {"id": "project:recommendation-engine", "name": "Recommendation Engine", "description": "An ML system that personalizes recommendations."},
                {"id": "project:api-gateway", "name": "API Gateway", "description": "A backend service for internal tooling."},
                {"id": "project:ops-dashboard", "name": "Ops Dashboard", "description": "A monitoring dashboard for deployment health."},
                {"id": "project:ml-pipeline", "name": "ML Pipeline", "description": "A pipeline for training and serving models."},
                {"id": "project:devex-portal", "name": "Developer Portal", "description": "A portal for internal developer productivity tools."},
                {"id": "project:search-ui", "name": "Search UI", "description": "A React-based search experience for customers."},
                {"id": "project:data-warehouse", "name": "Data Warehouse", "description": "A warehouse that consolidates product and engineering data."},
                {"id": "project:saas-analytics", "name": "SaaS Analytics", "description": "A reporting stack for SaaS operations."},
                {"id": "project:research-lab", "name": "Research Lab", "description": "A platform for exploring new algorithms."},
            ]})

            session.execute_write(run_query, """
                UNWIND $companies AS company
                MERGE (c:Company {id: company.id})
                SET c.name = company.name,
                    c.industry = company.industry
            """, {"companies": [
                {"id": "company:acme", "name": "Acme Analytics", "industry": "Data"},
                {"id": "company:brightlabs", "name": "BrightLabs", "industry": "AI"},
                {"id": "company:delta", "name": "Delta Systems", "industry": "Software"},
                {"id": "company:helio", "name": "Helio Cloud", "industry": "Cloud"},
                {"id": "company:vertex", "name": "Vertex Labs", "industry": "Research"},
                {"id": "company:novum", "name": "Novum Data", "industry": "Analytics"},
                {"id": "company:orbit", "name": "Orbit Software", "industry": "Software"},
                {"id": "company:stackline", "name": "Stackline", "industry": "Infrastructure"},
            ]})

            relationships = [
                ("person:ana", "HAS_SKILL", "skill:python"),
                ("person:ana", "HAS_SKILL", "skill:sql"),
                ("person:ana", "HAS_SKILL", "skill:statistics"),
                ("person:ana", "HAS_SKILL", "skill:tableau"),
                ("person:ben", "HAS_SKILL", "skill:python"),
                ("person:ben", "HAS_SKILL", "skill:pytorch"),
                ("person:ben", "HAS_SKILL", "skill:ml"),
                ("person:ben", "HAS_SKILL", "skill:testing"),
                ("person:chris", "HAS_SKILL", "skill:python"),
                ("person:chris", "HAS_SKILL", "skill:fastapi"),
                ("person:chris", "HAS_SKILL", "skill:redis"),
                ("person:chris", "HAS_SKILL", "skill:git"),
                ("person:dana", "HAS_SKILL", "skill:react"),
                ("person:dana", "HAS_SKILL", "skill:typescript"),
                ("person:dana", "HAS_SKILL", "skill:testing"),
                ("person:eli", "HAS_SKILL", "skill:docker"),
                ("person:eli", "HAS_SKILL", "skill:kubernetes"),
                ("person:eli", "HAS_SKILL", "skill:aws"),
                ("person:eli", "HAS_SKILL", "skill:linux"),
                ("person:fiona", "HAS_SKILL", "skill:analytics"),
                ("person:fiona", "HAS_SKILL", "skill:sql"),
                ("person:fiona", "HAS_SKILL", "skill:tableau"),
                ("person:greg", "HAS_SKILL", "skill:python"),
                ("person:greg", "HAS_SKILL", "skill:neo4j"),
                ("person:greg", "HAS_SKILL", "skill:cypher"),
                ("person:greg", "HAS_SKILL", "skill:airflow"),
                ("person:hina", "HAS_SKILL", "skill:sql"),
                ("person:hina", "HAS_SKILL", "skill:airflow"),
                ("person:hina", "HAS_SKILL", "skill:python"),
                ("person:ivy", "HAS_SKILL", "skill:python"),
                ("person:ivy", "HAS_SKILL", "skill:react"),
                ("person:ivy", "HAS_SKILL", "skill:fastapi"),
                ("person:jo", "HAS_SKILL", "skill:python"),
                ("person:jo", "HAS_SKILL", "skill:pytorch"),
                ("person:jo", "HAS_SKILL", "skill:ml"),
                ("person:jo", "HAS_SKILL", "skill:prometheus"),
                ("person:maya", "HAS_SKILL", "skill:python"),
                ("person:maya", "HAS_SKILL", "skill:sql"),
                ("person:maya", "HAS_SKILL", "skill:pandas"),
            ]

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (source {id: relationship.source}), (target {id: relationship.target})
                MERGE (source)-[:HAS_SKILL]->(target)
            """, {"relationships": [
                {"source": src, "target": tgt} for src, _, tgt in relationships
            ]})

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (person:Person {id: relationship.person}), (project:Project {id: relationship.project})
                MERGE (person)-[:WORKED_ON]->(project)
            """, {"relationships": [
                {"person": "person:ana", "project": "project:insight-platform"},
                {"person": "person:ben", "project": "project:recommendation-engine"},
                {"person": "person:chris", "project": "project:api-gateway"},
                {"person": "person:dana", "project": "project:search-ui"},
                {"person": "person:eli", "project": "project:ops-dashboard"},
                {"person": "person:fiona", "project": "project:saas-analytics"},
                {"person": "person:greg", "project": "project:data-warehouse"},
                {"person": "person:hina", "project": "project:ml-pipeline"},
                {"person": "person:ivy", "project": "project:devex-portal"},
                {"person": "person:jo", "project": "project:research-lab"},
            ]})

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (project:Project {id: relationship.project}), (technology:Technology {id: relationship.technology})
                MERGE (project)-[:USES]->(technology)
            """, {"relationships": [
                {"project": "project:insight-platform", "technology": "tech:tableau"},
                {"project": "project:recommendation-engine", "technology": "tech:pytorch"},
                {"project": "project:api-gateway", "technology": "tech:fastapi"},
                {"project": "project:search-ui", "technology": "tech:react"},
                {"project": "project:ops-dashboard", "technology": "tech:prometheus"},
                {"project": "project:ml-pipeline", "technology": "tech:airflow"},
                {"project": "project:devex-portal", "technology": "tech:docker"},
                {"project": "project:data-warehouse", "technology": "tech:neo4j"},
                {"project": "project:saas-analytics", "technology": "tech:aws"},
                {"project": "project:research-lab", "technology": "tech:python"},
            ]})

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (job_role:JobRole {id: relationship.job_role}), (skill:Skill {id: relationship.skill})
                MERGE (job_role)-[:REQUIRES]->(skill)
            """, {"relationships": [
                {"job_role": "jobrole:data-scientist", "skill": "skill:python"},
                {"job_role": "jobrole:data-scientist", "skill": "skill:statistics"},
                {"job_role": "jobrole:data-scientist", "skill": "skill:sql"},
                {"job_role": "jobrole:data-scientist", "skill": "skill:pytorch"},
                {"job_role": "jobrole:ml-engineer", "skill": "skill:python"},
                {"job_role": "jobrole:ml-engineer", "skill": "skill:ml"},
                {"job_role": "jobrole:ml-engineer", "skill": "skill:pytorch"},
                {"job_role": "jobrole:backend-engineer", "skill": "skill:python"},
                {"job_role": "jobrole:backend-engineer", "skill": "skill:fastapi"},
                {"job_role": "jobrole:backend-engineer", "skill": "skill:redis"},
                {"job_role": "jobrole:frontend-engineer", "skill": "skill:react"},
                {"job_role": "jobrole:frontend-engineer", "skill": "skill:typescript"},
                {"job_role": "jobrole:devops-engineer", "skill": "skill:docker"},
                {"job_role": "jobrole:devops-engineer", "skill": "skill:kubernetes"},
                {"job_role": "jobrole:data-engineer", "skill": "skill:sql"},
                {"job_role": "jobrole:data-engineer", "skill": "skill:airflow"},
                {"job_role": "jobrole:product-analyst", "skill": "skill:analytics"},
                {"job_role": "jobrole:research-engineer", "skill": "skill:python"},
                {"job_role": "jobrole:research-engineer", "skill": "skill:neo4j"},
                {"job_role": "jobrole:ai-engineer", "skill": "skill:python"},
                {"job_role": "jobrole:ai-engineer", "skill": "skill:ml"},
                {"job_role": "jobrole:software-engineer", "skill": "skill:python"},
                {"job_role": "jobrole:software-engineer", "skill": "skill:testing"},
            ]})

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (job_role:JobRole {id: relationship.job_role}), (technology:Technology {id: relationship.technology})
                MERGE (job_role)-[:USES]->(technology)
            """, {"relationships": [
                {"job_role": "jobrole:data-scientist", "technology": "tech:python"},
                {"job_role": "jobrole:data-scientist", "technology": "tech:tableau"},
                {"job_role": "jobrole:ml-engineer", "technology": "tech:pytorch"},
                {"job_role": "jobrole:ml-engineer", "technology": "tech:docker"},
                {"job_role": "jobrole:backend-engineer", "technology": "tech:fastapi"},
                {"job_role": "jobrole:backend-engineer", "technology": "tech:redis"},
                {"job_role": "jobrole:frontend-engineer", "technology": "tech:react"},
                {"job_role": "jobrole:frontend-engineer", "technology": "tech:typescript"},
                {"job_role": "jobrole:devops-engineer", "technology": "tech:kubernetes"},
                {"job_role": "jobrole:devops-engineer", "technology": "tech:aws"},
                {"job_role": "jobrole:data-engineer", "technology": "tech:airflow"},
                {"job_role": "jobrole:data-engineer", "technology": "tech:neo4j"},
                {"job_role": "jobrole:product-analyst", "technology": "tech:tableau"},
                {"job_role": "jobrole:research-engineer", "technology": "tech:python"},
                {"job_role": "jobrole:ai-engineer", "technology": "tech:pytorch"},
                {"job_role": "jobrole:software-engineer", "technology": "tech:git"},
            ]})

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (source:JobRole {id: relationship.source}), (target:JobRole {id: relationship.target})
                MERGE (source)-[:RELATED_TO]->(target)
            """, {"relationships": [
                {"source": "jobrole:data-scientist", "target": "jobrole:ml-engineer"},
                {"source": "jobrole:ml-engineer", "target": "jobrole:ai-engineer"},
                {"source": "jobrole:backend-engineer", "target": "jobrole:software-engineer"},
                {"source": "jobrole:frontend-engineer", "target": "jobrole:software-engineer"},
                {"source": "jobrole:devops-engineer", "target": "jobrole:backend-engineer"},
                {"source": "jobrole:data-engineer", "target": "jobrole:data-scientist"},
                {"source": "jobrole:product-analyst", "target": "jobrole:data-scientist"},
                {"source": "jobrole:research-engineer", "target": "jobrole:ml-engineer"},
            ]})

            session.execute_write(run_query, """
                UNWIND $relationships AS relationship
                MATCH (company:Company {id: relationship.company}), (job_role:JobRole {id: relationship.job_role})
                MERGE (company)-[:OFFERS]->(job_role)
            """, {"relationships": [
                {"company": "company:acme", "job_role": "jobrole:data-scientist"},
                {"company": "company:brightlabs", "job_role": "jobrole:ml-engineer"},
                {"company": "company:delta", "job_role": "jobrole:backend-engineer"},
                {"company": "company:delta", "job_role": "jobrole:frontend-engineer"},
                {"company": "company:helio", "job_role": "jobrole:devops-engineer"},
                {"company": "company:novum", "job_role": "jobrole:data-engineer"},
                {"company": "company:vertex", "job_role": "jobrole:research-engineer"},
                {"company": "company:orbit", "job_role": "jobrole:software-engineer"},
                {"company": "company:stackline", "job_role": "jobrole:devops-engineer"},
            ]})

            print("Seed data created successfully")
    finally:
        driver.close()


if __name__ == "__main__":
    create_graph()
