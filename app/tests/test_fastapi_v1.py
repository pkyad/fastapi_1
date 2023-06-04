import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status":True}
