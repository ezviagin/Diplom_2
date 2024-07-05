import pytest

from api.stellar_burger_api import User


@pytest.fixture(scope='function')
def user():
    user = User()
    user.create_user()
    yield user
    user.delete_user()


@pytest.fixture(scope='function')
def user_to_delete():
    user: User = None
    yield user
    if user:
        user.delete_user()
