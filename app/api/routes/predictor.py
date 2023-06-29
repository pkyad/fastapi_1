from pydantic import BaseModel
from db.models.administrator import AdministratorT
from fastapi import APIRouter, Depends, Request

from db.dependencies import get_db_session
from db.models.notes import Note, NoteT
from db.models.administrator import Tenant, TenantT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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


@router.get(
    "/notes/",
    response_model=list[NoteT],
    name="db-test:get-data",
)
async def read_notes(request: Request, db: AsyncSession = Depends(get_db_session)):
    q = await db.execute(Note.select())
    results = q.tuples()
    return [NoteT(id=r.id, text=r.text, completed=r.completed) for r in results]


from sqlalchemy.orm import selectinload


@router.get(
    "/tenant/",
    response_model=list[TenantT],
    name="db-test:get-data",
)
async def read_notes(request: Request, db: AsyncSession = Depends(get_db_session)):
    db.expire_on_commit = False
    q = await db.scalars(select(Tenant).options(selectinload(Tenant.users)))
    # print(q.all(), dir(q))
    # return q.all()

    # results = q.fetchall()
    # print("results", results)
    print("-----------------")
    return [
        TenantT(
            id=r.id,
            name=r.name,
            is_active=r.is_active,
            expiry_date=r.expiry_date,
            users=[
                AdministratorT(
                    id=admin.id,
                    name=admin.name,
                    email=admin.email,
                    is_active=admin.is_active,
                    is_admin=admin.is_admin,
                    is_staff=admin.is_staff,
                    password_change_required=admin.password_change_required,
                    next_password_change_due=admin.next_password_change_due,
                )
                for admin in r.users
            ],
        )
        for r in q
    ]


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
