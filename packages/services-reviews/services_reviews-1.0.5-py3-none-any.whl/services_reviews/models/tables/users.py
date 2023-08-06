from services_reviews.models.base import Base
from sqlalchemy import Column, Integer, String, BIGINT
from services_reviews.models.mixins import AuthMixin


class User(Base, AuthMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    branch_id = Column(BIGINT)

    def __init__(self, username, password, branch_id):
        self.username = username
        self.password = password
        self.branch_id = branch_id

    def __str__(self):
        return "User(id='%s')" % self.id


class RevokedTokenModel(Base, AuthMixin):
    __tablename__ = 'revoked_tokens'
    id = Column(Integer, primary_key=True)
    jti = Column(String(120))
