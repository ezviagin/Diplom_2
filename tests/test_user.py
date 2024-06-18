import pytest

from api.user import User
from helpers.faker import *


class TestCreateUser:
    def test_create_unique_user_success(self):
        user = User()
        response = user.create_user()
        assert response.status_code == 200
        assert response.json()['success'] is True

    def test_create_already_existing_user_failure(self):
        user = User()
        user.create_user()
        response = user.create_user(user.get_email(), 'UserPassword123!', user.get_name())
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
    def test_login_existing_user_success(self):
        user = User()
        user.create_user()
        response = user.login_user()
        assert response.status_code == 200
        assert response.json()['success'] is True

    @pytest.mark.parametrize('email', ['wrongemail@example.com!', ''])
    def test_login_bad_login_failure(self, email):
        user = User()
        creds = user.generate_user_credentials()
        response = user.login_user(email, creds.password)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'

    @pytest.mark.parametrize('password', ['BadPassword123!', ''])
    def test_login_bad_password_failure(self, password):
        user = User()
        creds = user.generate_user_credentials()
        response = user.login_user(creds.email, password)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'


class TestChangeUser:
    @pytest.mark.parametrize('new_email, new_password, new_name', [
        (generate_email(), None, None),
        (None, generate_password(), None),
        (None, None, generate_username()),
    ])
    def test_change_authorized_user_creds_success(self, new_email, new_password, new_name):
        user = User()
        user.create_user()
        user.login_user()
        response = user.change_user(email=new_email, password=new_password, name=new_name)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @pytest.mark.parametrize('new_email, new_password, new_name', [
        (generate_email(), None, None),
        (None, generate_password(), None),
        (None, None, generate_username()),
    ])
    def test_change_non_authorized_user_creds_failure(self, new_email, new_password, new_name):
        user = User()
        user.create_user()
        response = user.change_user(email=new_email, password=new_password, name=new_name)
        assert response.status_code == 401
        assert response.json()["success"] is False

    def test_change_already_used_email_failure(self):
        user = User()
        user.create_user()
        user.login_user()
        response = user.change_user(email=user.get_email())
        response = user.change_user(email=user.get_email())
        assert response.status_code == 403
        assert response.json()["success"] is False
