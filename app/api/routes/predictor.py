import json
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter()


class TestResponse(BaseModel):
    var1: str

class TestRequest(BaseModel):
    q: str

class HealthResponse(BaseModel):
    status: bool


@router.post(
    "/test1",
    response_model=TestResponse,
    name="predict:get-data",
)
async def predict(data_input: TestRequest):

    return TestResponse(var1=data_input.q)


@router.get(
    "/health",
    response_model=HealthResponse,
    name="health:get-data",
)
async def health():
    return HealthResponse(status=True)
