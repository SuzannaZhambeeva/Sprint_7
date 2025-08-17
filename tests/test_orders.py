import requests
import pytest
import allure
from helpers import ORDERS_URL


@allure.feature("Создание заказа")
class TestOrdersCreation:

    @allure.story("Можно указать BLACK, GREY, оба или ни одного цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Ivan",
            "lastName": "Ivanov",
            "address": "Moscow",
            "metroStation": "4",
            "phone": "+79999999999",
            "rentTime": 5,
            "deliveryDate": "2025-08-20",
            "comment": "test",
            "color": color
        }
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 201
        body = response.json()
        assert "track" in body and isinstance(body["track"], int), "Нет track в ответе"


@allure.feature("Список заказов")
class TestOrdersList:

    @allure.story("GET /orders возвращает список заказов")
    def test_get_orders_list(self):
        response = requests.get(ORDERS_URL)
        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
