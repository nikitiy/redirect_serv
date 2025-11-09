from sqlalchemy.ext.asyncio import AsyncSession

from src.redirect_serv.apps.company.models import CompanyBranch
from src.redirect_serv.apps.qr_manager.repositories import QRCodeRepository
from src.redirect_serv.core.exceptions import NotFoundError


class QRCodeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = QRCodeRepository(session)

    async def get_company_branch_and_increment_scan(
        self, url_hash: str
    ) -> CompanyBranch:
        qr_code = await self.repository.get_by_url_hash_with_branch(url_hash)
        if not qr_code:
            raise NotFoundError(f"QR code with hash '{url_hash}' not found")

        await self.repository.increment_scan_count(qr_code)

        return qr_code.company_branch
