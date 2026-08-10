from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

try:
    from backend.app.services.graph_service import (
        DatabaseUnavailableError,
        GraphServiceError,
        NotFoundError,
        get_job,
        get_job_skills,
        get_missing_skills,
        get_person_matches,
        get_person_name,
        get_skill_connections,
        list_jobs,
        list_people,
    )
except ModuleNotFoundError:  # pragma: no cover - supports running app from backend directory
    from app.services.graph_service import (
        DatabaseUnavailableError,
        GraphServiceError,
        NotFoundError,
        get_job,
        get_job_skills,
        get_missing_skills,
        get_person_matches,
        get_person_name,
        get_skill_connections,
        list_jobs,
        list_people,
    )

router = APIRouter(prefix="/api", tags=["careergraph"])


@router.get("/jobs")
def list_job_roles():
    try:
        return {"jobs": list_jobs()}
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


@router.get("/jobs/{job_id}")
def read_job(job_id: str):
    try:
        return get_job(job_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


@router.get("/jobs/{job_id}/skills")
def read_job_skills(job_id: str):
    try:
        return get_job_skills(job_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


@router.get("/people")
def read_people():
    try:
        return {"people": list_people()}
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


@router.get("/people/{person_id}/matches")
def read_person_matches(person_id: str):
    try:
        return {"person": get_person_name(person_id), "matches": get_person_matches(person_id)}
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


@router.get("/people/{person_id}/missing-skills/{job_id}")
def read_missing_skills(person_id: str, job_id: str):
    try:
        return get_missing_skills(person_id, job_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


@router.get("/skills/{skill_id}/connections")
def read_skill_connections(skill_id: str):
    try:
        return get_skill_connections(skill_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except GraphServiceError as exc:
        raise _handle_service_error(exc)


def _handle_service_error(exc: GraphServiceError) -> HTTPException:
    if isinstance(exc, DatabaseUnavailableError):
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")
