from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures.factories import CompanyFactory


@pytest_asyncio.fixture
async def _test_company(test_session: AsyncSession) -> AsyncGenerator:
    company = await CompanyFactory.create(
        session=test_session,
        name="Test Restaurant",
        subdomain="test-restaurant",
    )
    yield company
