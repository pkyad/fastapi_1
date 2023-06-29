import json
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from db.dependencies import get_db_session
from db.models.notes import notes
from sqlalchemy.ext.asyncio import AsyncSession


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


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


from fastapi import Request


@router.get(
    "/notes/",
    response_model=List[Note],
    name="db-test:get-data",
)
async def read_notes(request: Request, db: AsyncSession = Depends(get_db_session)):
    q = await db.execute(notes.select())
    results = q.tuples()
    return [Note(id=r.id, text=r.text, completed=r.completed) for r in results]
