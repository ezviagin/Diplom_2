import pytest

from api.order import *
from api.stellar_burger_api import User


@pytest.fixture(scope='class')
def created_user():
    user = User()
    user.create_user()
    yield user
    user.delete_user()


@pytest.fixture(scope='function')
def delete_user():
    user: User = None
    yield user
    if user:
        user.login_user()
        user.delete_user()
