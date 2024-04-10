import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Requ(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'req'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    content = sqlalchemy.Column(sqlalchemy.String)
    date_on = sqlalchemy.Column(sqlalchemy.DateTime)
    id_for = sqlalchemy.Column(sqlalchemy.Integer)  # , sqlalchemy.ForeignKey("users.id")
    id_in = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
