import pytest

from api.user import User


class TestCreateUser:
    def test_create_unique_user_success(self):
        user = User()
        response = user.create_user()
        assert response.status_code == 200 and response.json()['success'] is True

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
