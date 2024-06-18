import allure
from dataclasses import dataclass
import requests

from helpers.faker import *
from helpers.urls import *


@dataclass
class Credentials:
    email: str = ''
    password: str = ''
    name: str = ''


# noinspection PyTypeChecker
class User:
    def __init__(self):
        self.user_credentials: Credentials = None
        self.access_token: str = None
        self.refresh_token: str = None

    @staticmethod
    def generate_user_credentials() -> Credentials:
        return Credentials(
            email=generate_email(),
            password=generate_password(),
            name=generate_username(),
        )

    def get_email(self):
        return self.user_credentials.email

    def get_password(self):
        return self.user_credentials.password

    def get_name(self):
        return self.user_credentials.name

    def get_user_credentials(self) -> Credentials:
        return self.user_credentials

    @allure.step('Создание пользователя: POST /api/auth/register')
    def create_user(self, email: str = '', password: str = '', name: str = ''):
        if not email and not password and not name:
            self.user_credentials = self.generate_user_credentials()
        else:
            self.user_credentials = Credentials(email, password, name)

        return requests.post(f"{BASE_URL}{CREATE_USER}", json=self.user_credentials.__dict__)

    @allure.step('Удаление пользователя: DELETE /api/auth/user')
    def delete_user(self, access_token: str = None):
        token = access_token if access_token else self.access_token
        return requests.delete(f"{BASE_URL}{DELETE_USER}", headers={"Authorization": token})

    @allure.step('Авторизация пользователя: POST /api/auth/login')
    def login_user(self, email: str = '', password: str = ''):
        if not email and not password:
            payload = self.user_credentials.__dict__
        else:
            payload = {
                "email": email,
                "password": password,
            }

        response = requests.post(f"{BASE_URL}{LOGIN_USER}", json=payload)
        if response.status_code == 200:
            self.access_token = response.json()['accessToken']
            self.refresh_token = response.json()['refreshToken']

        return response

    def logout_user(self):
        payload = {
            "token": self.refresh_token
        }
        return requests.post(f"{BASE_URL}{LOGOUT_USER}", json=payload)

    @allure.step('Изменение данных пользователя: PATCH /api/auth/user')
    def change_user(self, email: str = None, password: str = None, name: str = None):
        email = email or self.get_email()
        password = password or self.get_password()
        name = name or self.get_name()

        payload = {
            "email": email,
            "password": password,
            "name": name,
        }

        response = requests.patch(f"{BASE_URL}{CHANGE_USER}",
                                  headers={"Authorization": self.access_token}, json=payload)
        if response.status_code == 200:
            self.user_credentials.email = email
            self.user_credentials.password = password
            self.user_credentials.name = name

        return response

    def update_token(self):
        payload = {
            "email": self.get_email(),
            "password": self.get_password(),
        }
        response = requests.post(f"{BASE_URL}{UPDATE_TOKEN}", json=payload)
        return response

    @allure.step('Создание заказа: POST /api/orders')
    def create_order(self, order: dict):
        return requests.post(f"{BASE_URL}{CREATE_ORDER}", json=order)

    @allure.step('Получение заказов конкретного пользователя: GET /api/orders')
    def get_user_orders(self, access_token: str = None):
        token = access_token if access_token else self.access_token
        return requests.get(f"{BASE_URL}{GET_ORDER}", headers={"Authorization": token})

    @staticmethod
    def get_all_orders():
        return requests.get(f"{BASE_URL}{GET_ALL_ORDERS}")

    @staticmethod
    def get_ingredients():
        return requests.get(f"{BASE_URL}{GET_INGREDIENTS}")

    @staticmethod
    def assemble_random_ingredients() -> dict:
        response = User().get_ingredients()
        if not response.ok:
            return {}

        data = response.json()
        if data.get('success') is not True:
            return {}

        id_list = [item['_id'] for item in data["data"]]

        return {"ingredients": random.sample(id_list, 3)}
