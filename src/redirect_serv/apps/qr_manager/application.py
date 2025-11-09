from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.redirect_serv.apps.qr_manager.services import QRCodeService
from src.redirect_serv.core.config import base_settings


class QRCodeApplication:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.qr_code_service = QRCodeService(session)

    async def redirect_qr_code(self, url_hash: str) -> RedirectResponse:
        company_branch = (
            await self.qr_code_service.get_company_branch_and_increment_scan(url_hash)
        )

        subdomain = company_branch.company.subdomain
        redirect_url = f"https://{subdomain}.{base_settings.guest_serv_domain}/"

        response = RedirectResponse(url=redirect_url, status_code=302)
        response.set_cookie(
            key="company_branch_id",
            value=str(company_branch.id),
            max_age=86400 * 30,  # 30 days
            httponly=True,
            secure=True,  # HTTPS only
            samesite="lax",  # CSRF protection
        )

        return response
