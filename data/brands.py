import sqlalchemy
from .db_session import SqlAlchemyBase


class Brands(SqlAlchemyBase):
    __tablename__ = 'brands'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


