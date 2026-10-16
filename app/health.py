from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlmodel import Session

from app import database, schemas

router = APIRouter(prefix="/health")

# Dependency to get a database session
SessionDep = Annotated[Session, Depends(database.get_session)]


@router.get("/live", summary="Liveness Health Check")
def liveness_check():
    """Liveness check endpoint. Returns 200 (OK) if application process is running."""
    return schemas.HealthCheck(status="OK")


@router.get("/ready", summary="Readiness Health Check")
def readiness_check(session: SessionDep):
    """Readiness check endpoint. Returns 200 (OK) if application can serve traffic."""
    # Test database connectivity
    try:
        session.exec(text("SELECT 1"))
        return schemas.HealthCheck(status="OK")
    # A readiness probe must report any failure as not ready, whatever raised it.
    except Exception as e:  # noqa: BLE001
        # Return 503 Service Unavailable if database is not accessible
        raise HTTPException(
            status_code=503, detail=f"Database connection failed: {e!s}"
        )
