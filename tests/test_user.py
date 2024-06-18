import pytest

from api.stellar_burger_api import User
from conftest import authorized_user, non_authorized_user, user_to_delete
from helpers.faker import *


class TestCreateUser:
    def test_create_unique_user_success(self, user_to_delete):
        user_to_delete = User()
        response = user_to_delete.create_user()
        assert response.status_code == 200
        assert response.json()['success'] is True

    def test_create_already_existing_user_failure(self):
        user = User()
        user.create_user()
        response = user.create_user(
            user.get_email(), 'UserPassword123!', user.get_name())
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @pytest.mark.parametrize('key', ['email', 'password', 'name'])
    def test_create_user_without_one_necessary_field_failure(self, key):
        user = User()
        creds = user.generate_user_credentials()
        setattr(creds, key, '')
        response = user.create_user(creds.email, creds.password, creds.name)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Email, password and name are required fields'


class TestLoginUser:
    def test_login_existing_user_success(self, non_authorized_user):
        response = non_authorized_user.login_user()
        assert response.status_code == 200
        assert response.json()['success'] is True

    @pytest.mark.parametrize('email', ['wrongemail@example.com!', ''])
    def test_login_bad_login_failure(self, non_authorized_user, email):
        creds = non_authorized_user.generate_user_credentials()
        response = non_authorized_user.login_user(email, creds.password)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'

    @pytest.mark.parametrize('password', ['BadPassword123!', ''])
    def test_login_bad_password_failure(self, non_authorized_user, password):
        creds = non_authorized_user.generate_user_credentials()
        response = non_authorized_user.login_user(creds.email, password)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'


class TestChangeUser:
    @pytest.mark.parametrize('new_email, new_password, new_name', [
        (generate_email(), None, None),
        (None, generate_password(), None),
        (None, None, generate_username()),
    ])
    def test_change_authorized_user_creds_success(self, authorized_user, new_email, new_password, new_name):
        response = authorized_user.change_user(email=new_email, password=new_password, name=new_name)
        assert response.status_code == 200
        assert response.json()['success'] is True

    @pytest.mark.parametrize('new_email, new_password, new_name', [
        (generate_email(), None, None),
        (None, generate_password(), None),
        (None, None, generate_username()),
    ])
    def test_change_non_authorized_user_creds_failure(self, non_authorized_user, new_email, new_password, new_name):
        response = non_authorized_user.change_user(email=new_email, password=new_password, name=new_name)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You should be authorised'

    def test_change_already_used_email_failure(self, authorized_user):
        user2 = User()
        user2.create_user()
        response = authorized_user.change_user(email=user2.get_email())
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User with such email already exists'
