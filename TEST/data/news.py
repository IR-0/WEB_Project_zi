import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    content = sqlalchemy.Column(sqlalchemy.String)
    data_on = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    id_whom = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
