from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    false
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=True)
    is_banned = Column(Boolean, nullable=False, default=False, server_default=false())
    subscribed_group = Column(Integer, nullable=True)


class SubscribedGroup(Base):
    __tablename__ = 'subscribed_groups'

    id = Column(Integer, primary_key=True)
    group_id = Column(BigInteger, nullable=False, unique=True, index=True) 
    subscribed_group = Column(Integer, nullable=True)

