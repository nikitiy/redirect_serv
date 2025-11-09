from typing import AsyncGenerator

import httpx
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import JSON, DateTime, Table
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.redirect_serv.apps.company.models import Company, CompanyBranch
from src.redirect_serv.apps.qr_manager.models import QRCode
from src.redirect_serv.core.app import create_app
from src.redirect_serv.core.dependencies.database import get_session
from tests.fixtures.factories import CompanyFactory


def adapt_table_for_sqlite(table: Table) -> None:
    """Adapt PostgreSQL-specific types to SQLite-compatible types"""
    for column in table.columns:
        if isinstance(column.type, JSONB):
            column.type = JSON()
        elif isinstance(column.type, TIMESTAMP):
            column.type = DateTime()


@pytest_asyncio.fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    tables_to_create = [
        Company.__table__,
        CompanyBranch.__table__,
        QRCode.__table__,
    ]

    async with engine.begin() as conn:
        for table in tables_to_create:
            adapt_table_for_sqlite(table)
            await conn.run_sync(table.create, checkfirst=True)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        for table in reversed(tables_to_create):
            await conn.run_sync(table.drop, checkfirst=True)

    await engine.dispose()


@pytest_asyncio.fixture
async def test_app(test_session: AsyncSession) -> AsyncGenerator[FastAPI, None]:
    app = create_app()

    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    yield app

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(test_app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_company(test_session: AsyncSession) -> AsyncGenerator:
    company = await CompanyFactory.create(
        session=test_session,
        name="Test Restaurant",
        subdomain="test-restaurant",
    )
    yield company
