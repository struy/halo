import pytest
from models import User


@pytest.fixture(scope='module')
def new_user():
    user = User('Alexa', 'AWS')
    return user
