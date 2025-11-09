from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.redirect_serv.api.health import router as health_router
from src.redirect_serv.core.config import cors_settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Redirect_serv API",
        description="API for redirect_serv",
        version="0.1.0",
    )

    if cors_settings.enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_settings.allow_origins,
            allow_credentials=cors_settings.allow_credentials,
            allow_methods=cors_settings.allow_methods,
            allow_headers=cors_settings.allow_headers,
        )

    # Routers
    app.include_router(health_router)

    return app


__all__ = ("create_app",)
