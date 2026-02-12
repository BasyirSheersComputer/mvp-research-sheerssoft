import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import engine
from app.models import Base

# Remove manual event_loop fixture to let pytest-asyncio handle it

@pytest.fixture(scope="function")
async def client():
    """
    Async HTTP client for testing the FastAPI app.
    Function scope matches the default pytest-asyncio loop scope.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """
    Ensure database tables exist before running tests.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
