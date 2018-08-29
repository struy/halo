from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, \
    check_password_hash

engine = create_engine('sqlite:///main.db', echo=False)
Base = declarative_base()


########################################################################

class User(Base):
    """
    User: username, password (hashed)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    entities = relationship('Entity', backref='user',
                            lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # ----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


########################################################################

class Entity(Base):
    """
    Entity of key/value pair of current User
    """
    __tablename__ = "entities"

    key = Column(String, primary_key=True)
    value = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'key': self.key,
            'value': self.value
        }

    # ----------------------------------------------------------------------
    def __init__(self, key, value, user_id):
        """"""
        self.key = key
        self.value = value
        self.user_id = user_id

    def __repr__(self):
        return '<Entity:  {} / {}>'.format(self.key, self.value)


# create tables
Base.metadata.create_all(engine)
