import hashlib
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.redirect_serv.apps.company.models import Company, CompanyBranch
from src.redirect_serv.apps.qr_manager.models import QRCode


class CompanyFactory:
    @staticmethod
    async def create(
        session: AsyncSession,
        name: str = "Test Restaurant",
        subdomain: str = "test-restaurant",
        commit: bool = True,
    ) -> Company:
        company = Company(
            name=name,
            subdomain=subdomain,
        )
        session.add(company)
        if commit:
            await session.commit()
            await session.refresh(company)
        return company


class CompanyBranchFactory:
    @staticmethod
    async def create(
        session: AsyncSession,
        company_id: int,
        commit: bool = True,
    ) -> CompanyBranch:
        branch = CompanyBranch(
            company_id=company_id,
        )
        session.add(branch)
        if commit:
            await session.commit()
            await session.refresh(branch)
        return branch


class QRCodeFactory:
    @staticmethod
    async def create(
        session: AsyncSession,
        company_branch_id: int,
        url_hash: Optional[str] = None,
        qr_options: Optional[dict] = None,
        scan_count: int = 0,
        commit: bool = True,
    ) -> QRCode:
        if url_hash is None:
            url_hash = hashlib.sha256(str(company_branch_id).encode()).hexdigest()

        qr_code = QRCode(
            company_branch_id=company_branch_id,
            url_hash=url_hash,
            qr_options=qr_options or {},
            scan_count=scan_count,
        )
        session.add(qr_code)
        if commit:
            await session.commit()
            await session.refresh(qr_code)
        return qr_code
