import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.redirect_serv.apps.qr_manager.application import QRCodeApplication
from src.redirect_serv.apps.qr_manager.services import QRCodeService


@pytest_asyncio.fixture
async def qr_code_service(test_session: AsyncSession) -> QRCodeService:
    return QRCodeService(test_session)


@pytest_asyncio.fixture
async def qr_code_application(test_session: AsyncSession) -> QRCodeApplication:
    return QRCodeApplication(test_session)
