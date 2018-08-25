from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///main.db', echo=True)
Base = declarative_base()


########################################################################

class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    entities = relationship('Entity', backref='user',
                            lazy='dynamic')

    # ----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password


########################################################################

class Entity(Base):
    """"""
    __tablename__ = "entities"

    key = Column(String, primary_key=True)
    value = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    # ----------------------------------------------------------------------
    def __init__(self, key, value, user_id):
        """"""
        self.key = key
        self.value = value
        self.user_id = user_id


# create tables
Base.metadata.create_all(engine)
