from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlmodel import Session
from app import schemas, database

router = APIRouter(prefix="/health")


@router.get("/live", summary="Liveness Health Check")
def liveness_check():
    """Liveness check endpoint. Returns 200 (OK) if application process is running."""
    return schemas.HealthCheck(status="OK")


@router.get("/ready", summary="Readiness Health Check")
def readiness_check(session: Session = Depends(database.get_session)):
    """Readiness check endpoint. Returns 200 (OK) if application can serve traffic."""
    # Test database connectivity
    try:
        session.exec(text("SELECT 1"))
        return schemas.HealthCheck(status="OK")
    except Exception as e:
        # Return 503 Service Unavailable if database is not accessible
        raise HTTPException(
            status_code=503, detail=f"Database connection failed: {str(e)}"
        )
