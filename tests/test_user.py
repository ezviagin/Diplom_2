import allure
import pytest

from api.stellar_burger_api import User
from conftest import user, user_to_delete
from helpers.faker import *
from helpers.replies import *


@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Успешное создание уникального пользователя')
    @allure.description('Проверка успешного создания уникального пользователя')
    def test_create_unique_user_success(self, user_to_delete):
        user_to_delete = User()
        response = user_to_delete.create_user()
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Неуспешное создание уже существующего пользователя')
    @allure.description('Проверка ошибки при создании уже существующего пользователя')
    def test_create_already_existing_user_failure(self):
        user = User()
        user.create_user()
        response = user.create_user(
            user.get_email(), 'UserPassword123!', user.get_name())
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == USER_ALREADY_EXISTS

    @allure.title('Неуспешное создание пользователя без одного обязательного поля')
    @allure.description('Проверка ошибки при создании пользователя без одного обязательного поля')
    @pytest.mark.parametrize('key', ['email', 'password', 'name'])
    def test_create_user_without_one_necessary_field_failure(self, key):
        user = User()
        creds = user.generate_user_credentials()
        setattr(creds, key, '')
        response = user.create_user(creds.email, creds.password, creds.name)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == EMAIL_PASSWORD_NAME_REQUIRED


@allure.feature('Вход пользователя')
class TestLoginUser:
    @allure.title('Успешный вход существующего пользователя')
    @allure.description('Проверка успешного входа существующего пользователя')
    def test_login_existing_user_success(self, user):
        response = user.login_user()
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Неуспешный вход с неверным логином')
    @allure.description('Проверка ошибки при входе с неверным логином')
    @pytest.mark.parametrize('email', ['wrongemail@example.com!', ''])
    def test_login_bad_login_failure(self, user, email):
        creds = user.generate_user_credentials()
        response = user.login_user(email, creds.password)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == EMAIL_OR_PASSWORD_INCORRECT

    @allure.title('Неуспешный вход с неверным паролем')
    @allure.description('Проверка ошибки при входе с неверным паролем')
    @pytest.mark.parametrize('password', ['BadPassword123!', ''])
    def test_login_bad_password_failure(self, user, password):
        creds = user.generate_user_credentials()
        response = user.login_user(creds.email, password)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == EMAIL_OR_PASSWORD_INCORRECT


@allure.feature('Изменение данных пользователя')
class TestChangeUser:
    @allure.title('Успешное изменение данных пользователя')
    @allure.description('Проверка успешного изменения данных пользователя')
    @pytest.mark.parametrize('new_email, new_password, new_name', [
        (generate_email(), None, None),
        (None, generate_password(), None),
        (None, None, generate_username()),
    ])
    def test_change_user_creds_success(self, user, new_email, new_password, new_name):
        user.login_user()
        response = user.change_user(email=new_email, password=new_password, name=new_name)
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Неуспешное изменение данных пользователя без авторизации')
    @allure.description('Проверка на ошибку при изменении данных пользователя без авторизации')
    @pytest.mark.parametrize('new_email, new_password, new_name', [
        (generate_email(), None, None),
        (None, generate_password(), None),
        (None, None, generate_username()),
    ])
    def test_change_user_creds_failure(self, user, new_email, new_password, new_name):
        response = user.change_user(email=new_email, password=new_password, name=new_name)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == AUTH_REQUIRED

    @allure.title('Неуспешное изменение email на уже используемый')
    @allure.description('Проверка на ошибку при изменении email на уже используемый')
    def test_change_already_used_email_failure(self, user):
        user2 = User()
        user2.create_user()
        user.login_user()
        response = user.change_user(email=user2.get_email())
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == USER_WITH_EMAIL_ALREADY_EXISTS
