import pytest
from httpx import AsyncClient
from typing import Any, AsyncGenerator
from fastapi import FastAPI
from app.main import get_application

print('setting up fixures')
@pytest.fixture
def fastapi_app(
    # dbsession: AsyncSession,
    # fake_redis_pool: ConnectionPool,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_application()
    # application.dependency_overrides[get_db_session] = lambda: dbsession
    # application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
