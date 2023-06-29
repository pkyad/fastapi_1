import sqlalchemy as sa

meta = sa.MetaData()

from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    pass
