import hashlib
from unittest.mock import MagicMock, patch

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures.factories import CompanyBranchFactory, QRCodeFactory


@pytest.mark.asyncio
async def test_redirect_qr_code_success(
    client: httpx.AsyncClient,
    test_session: AsyncSession,
    test_company,
):
    branch = await CompanyBranchFactory.create(
        session=test_session,
        company_id=test_company.id,
    )

    url_hash = hashlib.sha256(str(branch.id).encode()).hexdigest()
    await QRCodeFactory.create(
        session=test_session,
        company_branch_id=branch.id,
        url_hash=url_hash,
    )

    mock_settings = MagicMock()
    mock_settings.guest_serv_domain = "localhost"
    mock_settings.redirect_protocol = "http"
    mock_settings.use_https = False

    with patch(
        "src.redirect_serv.apps.qr_manager.application.base_settings", mock_settings
    ):
        response = await client.get(f"/redirect/{url_hash}", follow_redirects=False)

        assert response.status_code == 302
        assert (
            response.headers["location"]
            == f"http://{test_company.subdomain}.localhost/"
        )

        cookies = response.cookies
        assert "company_branch_id" in cookies
        assert cookies["company_branch_id"] == str(branch.id)


@pytest.mark.asyncio
async def test_redirect_qr_code_not_found(
    client: httpx.AsyncClient,
    test_session: AsyncSession,
):
    url_hash = hashlib.sha256("99999".encode()).hexdigest()

    response = await client.get(f"/redirect/{url_hash}")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_redirect_qr_code_increments_scan_count(
    client: httpx.AsyncClient,
    test_session: AsyncSession,
    test_company,
):
    branch = await CompanyBranchFactory.create(
        session=test_session,
        company_id=test_company.id,
    )

    url_hash = hashlib.sha256(str(branch.id).encode()).hexdigest()
    qr_code = await QRCodeFactory.create(
        session=test_session,
        company_branch_id=branch.id,
        url_hash=url_hash,
        scan_count=0,
    )

    initial_scan_count = qr_code.scan_count

    mock_settings = MagicMock()
    mock_settings.guest_serv_domain = "localhost"
    mock_settings.redirect_protocol = "http"
    mock_settings.use_https = False

    with patch(
        "src.redirect_serv.apps.qr_manager.application.base_settings", mock_settings
    ):
        response = await client.get(f"/redirect/{url_hash}", follow_redirects=False)

        assert response.status_code == 302

        await test_session.refresh(qr_code)
        assert qr_code.scan_count == initial_scan_count + 1


@pytest.mark.asyncio
async def test_redirect_qr_code_with_https(
    client: httpx.AsyncClient,
    test_session: AsyncSession,
    test_company,
):
    branch = await CompanyBranchFactory.create(
        session=test_session,
        company_id=test_company.id,
    )

    url_hash = hashlib.sha256(str(branch.id).encode()).hexdigest()
    await QRCodeFactory.create(
        session=test_session,
        company_branch_id=branch.id,
        url_hash=url_hash,
    )

    mock_settings = MagicMock()
    mock_settings.guest_serv_domain = "example.com"
    mock_settings.redirect_protocol = "https"
    mock_settings.use_https = True

    with patch(
        "src.redirect_serv.apps.qr_manager.application.base_settings", mock_settings
    ):

        response = await client.get(f"/redirect/{url_hash}", follow_redirects=False)

        assert response.status_code == 302
        assert (
            response.headers["location"]
            == f"https://{test_company.subdomain}.example.com/"
        )

        set_cookie_header = response.headers.get("set-cookie", "")
        assert "Secure" in set_cookie_header


@pytest.mark.asyncio
async def test_redirect_qr_code_cookie_attributes(
    client: httpx.AsyncClient,
    test_session: AsyncSession,
    test_company,
):
    branch = await CompanyBranchFactory.create(
        session=test_session,
        company_id=test_company.id,
    )

    url_hash = hashlib.sha256(str(branch.id).encode()).hexdigest()
    await QRCodeFactory.create(
        session=test_session,
        company_branch_id=branch.id,
        url_hash=url_hash,
    )

    mock_settings = MagicMock()
    mock_settings.guest_serv_domain = "localhost"
    mock_settings.redirect_protocol = "http"
    mock_settings.use_https = False

    with patch(
        "src.redirect_serv.apps.qr_manager.application.base_settings", mock_settings
    ):
        response = await client.get(f"/redirect/{url_hash}", follow_redirects=False)

        assert response.status_code == 302

        set_cookie_header = response.headers.get("set-cookie", "")

        assert "HttpOnly" in set_cookie_header
        assert "SameSite=lax" in set_cookie_header
        assert "Max-Age=2592000" in set_cookie_header  # 30 days
