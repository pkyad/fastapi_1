import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.anyio
async def test_read_main(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": True}


@pytest.mark.anyio
async def test_read_main(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 2
