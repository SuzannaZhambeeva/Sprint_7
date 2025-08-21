import pytest
import requests
import allure
from data import ORDERS_URL, DEFAULT_ORDER
from utils import generate_random_string

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.step("Создаем заказ с разными цветами")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_various_colors(self, color):
        payload = DEFAULT_ORDER.copy()
        payload["firstName"] = generate_random_string()
        payload["lastName"] = generate_random_string()
        payload["color"] = color

        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)


@allure.feature("Получение списка заказов")
class TestOrdersList:

    @allure.step("Получаем список всех заказов")
    def test_get_orders_list(self):
        response = requests.get(ORDERS_URL)
        assert response.status_code == 200
        orders = response.json().get("orders")
        assert isinstance(orders, list)
        allure.attach(str(orders), name="Orders List", attachment_type=allure.attachment_type.JSON)
