import pytest

from api.stellar_burger_api import User


@pytest.fixture(scope='class')
def authorized_user():
    user = User()
    user.create_user()
    user.login_user()
    yield user
    user.logout_user()
    user.delete_user()


@pytest.fixture(scope='class')
def non_authorized_user():
    user = User()
    user.create_user()
    yield user
    user.delete_user()


@pytest.fixture(scope='function')
def user_to_delete():
    user: User = None
    yield user
    if user:
        user.logout_user()
        user.delete_user()
