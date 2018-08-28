from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from faker import Faker

fake = Faker()

engine = create_engine('sqlite:///main.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin", "password")
session.add(user)

user = User("Alex", "Dubovyk")
session.add(user)

# commit the record the database
session.commit()

for i in range(1,3):
    for key, value in fake.pydict(10, True).items():
        session.add(Entity(key, str(value), i))
    session.commit()
