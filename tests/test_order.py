import allure
import pytest

from api.stellar_burger_api import User
from helpers.replies import *
from conftest import user


@allure.feature('Создание заказов')
class TestCreateOrder:
    @allure.title('Заказ с авторизацией')
    @allure.description('Создание заказа с авторизацией')
    def test_create_order_with_auth_success(self, user):
        user.login_user()
        order_list = user.assemble_random_ingredients()
        response = user.create_order(order_list)
        assert response.status_code == 200
        assert response.json()['success'] is True

    # Тест всегда завершается с кодом 200, согласно документации должен быть 400.
    # Наставник рекомендовал оставить комментарий в коде.
    @allure.title('Заказ без авторизации')
    @allure.description('Создание заказа без авторизации')
    def test_create_order_with_no_auth_failure(self, user):
        response = user.create_order(User().assemble_random_ingredients())
        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.title('Заказ без ингредиентов')
    @allure.description('Создание заказа без ингредиентов')
    def test_create_order_with_no_ingredients_failure(self, user):
        user.login_user()
        response = user.create_order({"ingredients": []})
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == INGREDIENT_ID_MUST_BE_PROVIDED

    @allure.title('Заказ с неверным хешем ингредиентов')
    @allure.description('Создание заказа с неверным хешем ингредиентов')
    @pytest.mark.parametrize('bad_hash', ['60d3b41abdacab0026a733', 'xxxxxxxxxx', 'dead', '0'])
    def test_create_order_with_bad_ingredient_failure(self, user, bad_hash):
        order_bad_hash = {"ingredients": bad_hash}
        user.login_user()
        response = user.create_order(order_bad_hash)
        assert response.status_code == 500


@allure.feature('Получение заказов')
class TestGetOrder:
    @allure.title('Получение заказов авторизованного пользователя')
    @allure.description('Получение заказов конкретного авторизованного пользователя')
    def test_get_orders_of_auth_user(self, user):
        user.login_user()
        for _ in (1, 10):
            user.create_order(User().assemble_random_ingredients())

        response = user.get_user_orders()
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Получение заказов неавторизованного пользователя')
    @allure.description('Получение заказов конкретного неавторизованного пользователя')
    def test_get_orders_of_non_auth_user(self, user):
        response = user.get_user_orders()
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == AUTH_REQUIRED

    @allure.title('Максимальное количество заказов')
    @allure.description('Проверка, что отображаются последние 50 заказов из выборки всех заказов')
    def test_get_max_num_of_all_orders(self):
        response = User().get_all_orders()
        order_list_len = len(response.json()['orders'])
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert order_list_len == 50
