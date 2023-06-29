from db.meta import meta
import sqlalchemy

notes = sqlalchemy.Table(
    "notes",
    meta,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)
