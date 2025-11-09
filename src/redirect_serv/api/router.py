from fastapi import APIRouter

from src.redirect_serv.api.qr_code import router as qr_code_router

api_router = APIRouter()

# QR Code routes
api_router.include_router(qr_code_router)

__all__ = ("api_router",)
