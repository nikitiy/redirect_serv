from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from src.redirect_serv.core.dependencies.database import engine

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness():
    return {"status": "ok"}


@router.get("/ready")
async def readiness():
    checks = {
        "database": False,
    }

    errors = []

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.scalar()
        checks["database"] = True
    except Exception as e:
        errors.append(f"Database check failed: {str(e)}")

    if not checks["database"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "checks": checks,
                "errors": errors,
            },
        )

    return {
        "status": "ready",
        "checks": checks,
    }
