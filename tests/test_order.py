import allure
import pytest

from api.stellar_burger_api import User
from conftest import authorized_user, non_authorized_user


class TestCreateOrder:
    @allure.description('Создание заказа с авторизацией')
    def test_create_order_with_auth_success(self, authorized_user):
        order_list = authorized_user.assemble_random_ingredients()
        response = authorized_user.create_order(order_list)
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.description('Создание заказа без авторизации')
    def test_create_order_with_no_auth_failure(self, non_authorized_user):
        response = non_authorized_user.create_order(User().assemble_random_ingredients())
        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.description('Создание заказа без ингредиентов')
    def test_create_order_with_no_ingredients_failure(self, authorized_user):
        response = authorized_user.create_order({"ingredients": []})
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.description('Создание заказа с неверным хешем ингредиентов')
    @pytest.mark.parametrize('bad_hash', ['61deaddeaddead1d', 'xxxxxxxxxx', 'dead', '0'])
    def test_create_order_with_bad_ingredient_failure(self, authorized_user, bad_hash):
        order_bad_hash = {"ingrediends": bad_hash}
        response = authorized_user.create_order(order_bad_hash)
        assert response.status_code == 500


class TestGetOrder:
    @allure.description('Получение заказов конкретного авторизованного пользователя')
    def test_get_orders_of_auth_user(self, authorized_user):
        for _ in (1, 10):
            authorized_user.create_order(User().assemble_random_ingredients())

        response = authorized_user.get_user_orders()
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.description('Получение заказов конкретного неавторизованного пользователя')
    def test_get_orders_of_non_auth_user(self, non_authorized_user):
        response = non_authorized_user.get_user_orders()
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == 'You should be authorised'

    def test_get_max_num_of_orders_success(self, authorized_user):
        for _ in (1, 10):
            authorized_user.create_order(User().assemble_random_ingredients())

        response = authorized_user.get_user_orders()
        # TODO
        order_list_len = len(response.json()['orders'])
        assert 50

    def test_get_max_num_of_all_orders(self):
        response = User().get_all_orders()
        order_list_len = len(response.json()['orders'])
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert order_list_len == 50
