from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.redirect_serv.apps.company.models.company_branch import CompanyBranch
from src.redirect_serv.apps.qr_manager.models import QRCode


class QRCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_url_hash_with_branch(self, url_hash: str) -> Optional[QRCode]:
        result = await self.session.execute(
            select(QRCode)
            .where(QRCode.url_hash == url_hash)
            .options(
                selectinload(QRCode.company_branch).selectinload(CompanyBranch.company)
            )
        )
        return result.scalar_one_or_none()

    async def increment_scan_count(self, qr_code: QRCode) -> None:
        from datetime import datetime, timezone

        qr_code.scan_count += 1
        qr_code.last_scanned = datetime.now(timezone.utc)
        await self.session.commit()
