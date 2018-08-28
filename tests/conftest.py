import pytest
from app.models import User
# from app import create_app


@pytest.fixture(scope='module')
def new_user():
    user = User('Alexa', 'AWS')
    return user





