from db.meta import meta
import sqlalchemy
from pydantic import BaseModel


notes = sqlalchemy.Table(
    "notes",
    meta,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


class NoteT(BaseModel):
    id: int
    text: str
    completed: bool
