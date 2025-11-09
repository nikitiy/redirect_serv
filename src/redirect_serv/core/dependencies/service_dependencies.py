from typing import Annotated, TypeAlias

from fastapi import Depends

from src.redirect_serv.apps.qr_manager.application import QRCodeApplication
from src.redirect_serv.core.dependencies.database import SessionDep

# ==================== SERVICE DEPENDENCIES ====================


async def get_qr_code_application(session: SessionDep) -> QRCodeApplication:
    return QRCodeApplication(session)


# ==================== ANNOTATED TYPES ====================

# QR Code Application
QRCodeApplicationDep: TypeAlias = Annotated[
    QRCodeApplication, Depends(get_qr_code_application)
]
