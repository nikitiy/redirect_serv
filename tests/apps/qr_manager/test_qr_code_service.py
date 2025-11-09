import hashlib
from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.redirect_serv.apps.qr_manager.services import QRCodeService
from src.redirect_serv.core.exceptions import NotFoundError
from tests.fixtures.factories import CompanyBranchFactory, QRCodeFactory


@pytest.mark.asyncio
async def test_get_company_branch_and_increment_scan_success(
    qr_code_service: QRCodeService,
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
    initial_last_scanned = qr_code.last_scanned

    result = await qr_code_service.get_company_branch_and_increment_scan(url_hash)

    assert result.id == branch.id
    assert result.company_id == test_company.id

    await test_session.refresh(qr_code)
    assert qr_code.scan_count == initial_scan_count + 1
    assert qr_code.last_scanned is not None
    assert qr_code.last_scanned != initial_last_scanned


@pytest.mark.asyncio
async def test_get_company_branch_and_increment_scan_not_found(
    qr_code_service: QRCodeService,
):
    url_hash = hashlib.sha256("99999".encode()).hexdigest()

    with pytest.raises(NotFoundError) as exc_info:
        await qr_code_service.get_company_branch_and_increment_scan(url_hash)

    assert "not found" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_get_company_branch_and_increment_scan_multiple_scans(
    qr_code_service: QRCodeService,
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
        scan_count=5,
    )

    # First scan
    await qr_code_service.get_company_branch_and_increment_scan(url_hash)
    await test_session.refresh(qr_code)
    assert qr_code.scan_count == 6

    # Second scan
    await qr_code_service.get_company_branch_and_increment_scan(url_hash)
    await test_session.refresh(qr_code)
    assert qr_code.scan_count == 7

    # Third scan
    await qr_code_service.get_company_branch_and_increment_scan(url_hash)
    await test_session.refresh(qr_code)
    assert qr_code.scan_count == 8


@pytest.mark.asyncio
async def test_get_company_branch_and_increment_scan_updates_last_scanned(
    qr_code_service: QRCodeService,
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
    )

    assert qr_code.last_scanned is None

    await qr_code_service.get_company_branch_and_increment_scan(url_hash)

    await test_session.refresh(qr_code)
    assert qr_code.last_scanned is not None
    assert isinstance(qr_code.last_scanned, datetime)


@pytest.mark.asyncio
async def test_get_company_branch_and_increment_scan_returns_correct_branch(
    qr_code_service: QRCodeService,
    test_session: AsyncSession,
    test_company,
):
    branch1 = await CompanyBranchFactory.create(
        session=test_session,
        company_id=test_company.id,
    )

    branch2 = await CompanyBranchFactory.create(
        session=test_session,
        company_id=test_company.id,
    )

    url_hash1 = hashlib.sha256(str(branch1.id).encode()).hexdigest()
    url_hash2 = hashlib.sha256(str(branch2.id).encode()).hexdigest()

    await QRCodeFactory.create(
        session=test_session,
        company_branch_id=branch1.id,
        url_hash=url_hash1,
    )

    await QRCodeFactory.create(
        session=test_session,
        company_branch_id=branch2.id,
        url_hash=url_hash2,
    )

    result1 = await qr_code_service.get_company_branch_and_increment_scan(url_hash1)
    result2 = await qr_code_service.get_company_branch_and_increment_scan(url_hash2)

    assert result1.id == branch1.id
    assert result2.id == branch2.id
    assert result1.id != result2.id
