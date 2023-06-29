from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends

from db.dependencies import get_db_session
from db.models.notes import notes, NoteT
from sqlalchemy.ext.asyncio import AsyncSession
from cache.dependency import get_redis_pool
from redis.asyncio import ConnectionPool, Redis

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


from fastapi import Request


@router.get(
    "/notes/",
    response_model=list[NoteT],
    name="db-test:get-data",
)
async def read_notes(request: Request, db: AsyncSession = Depends(get_db_session)):
    q = await db.execute(notes.select())
    results = q.tuples()
    return [NoteT(id=r.id, text=r.text, completed=r.completed) for r in results]


@router.get(
    "/cache-test/",
    response_model=str,
    name="db-test:get-data-from-cache",
)
async def read_cache(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    async with Redis(connection_pool=redis_pool) as redis:
        await redis.set("mykey", "cached-val")
        data = await redis.get("mykey")
    return data
