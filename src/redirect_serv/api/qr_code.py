from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.redirect_serv.core.dependencies import QRCodeApplicationDep

router = APIRouter()


@router.get("/redirect/{hash}")
async def redirect_qr_code(
    hash: str, application: QRCodeApplicationDep
) -> RedirectResponse:
    """Handle QR code redirect request"""
    return await application.redirect_qr_code(hash)
