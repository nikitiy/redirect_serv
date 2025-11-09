from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.redirect_serv.core.exceptions import NotFoundError


async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )
