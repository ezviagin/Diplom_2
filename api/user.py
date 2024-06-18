from dataclasses import dataclass
import requests


from helpers.faker import *
from helpers.urls import *


@dataclass
class Credentials:
    email: str = ''
    password: str = ''
    name: str = ''


class User:
    def __init__(self):
        self.user_credentials: Credentials = None

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

    def create_user(self, email: str = '', password: str = '', name: str = ''):
        if not email and not password and not name:
            self.user_credentials = self.generate_user_credentials()
        else:
            self.user_credentials = Credentials(email, password, name)

        return requests.post(f"{BASE_URL}{CREATE_USER}", json=self.user_credentials.__dict__)

    def login_user(self):
        return
