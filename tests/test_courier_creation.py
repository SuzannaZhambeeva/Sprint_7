import requests
import pytest
import allure
from helpers import register_new_courier_and_return_login_password, COURIER_URL

@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.story("Курьера можно создать; успешный ответ и тело {\"ok\": true}")
    def test_create_courier_success(self):
        creds = register_new_courier_and_return_login_password()
        assert creds, "Курьер не создался"

        login, password, first_name = creds

        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(COURIER_URL, json=payload)

        assert response.status_code in [201, 409], f"Ожидали 201 или 409, получили {response.status_code}"

        if response.status_code == 201:
            body = response.json()
            assert "ok" in body and body["ok"] is True, "Тело ответа не содержит {'ok': true}"

    @allure.story("Нельзя создать двух одинаковых курьеров; код 409 и ошибка")
    def test_create_same_courier_twice_fails(self):
        login, password, first_name = register_new_courier_and_return_login_password()
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(COURIER_URL, json=payload)

        assert response.status_code == 409, f"Ожидали 409, получили {response.status_code}"
        body = response.json()
        assert "message" in body, "Нет поля message в ошибке"
        assert body["message"], "Сообщение об ошибке пустое"

    @allure.story("Чтобы создать курьера, нужны обязательные поля; код 400")
    @pytest.mark.parametrize("payload", [
        {"password": "123456", "firstName": "Ivan"},
        {"login": "testuser", "firstName": "Ivan"},
    ])
    def test_create_courier_missing_fields(self, payload):
        response = requests.post(COURIER_URL, json=payload)

        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"

        body = response.json()
        assert "message" in body, "Нет поля message в ошибке"
        assert body["message"], "Сообщение об ошибке пустое"
