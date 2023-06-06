import pytest
# from fastapi.testclient import TestClient
from app.main import app
from httpx import AsyncClient
from fastapi import FastAPI
from app.tests.testconf import *

@pytest.mark.anyio
async def test_read_main(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status":True}
