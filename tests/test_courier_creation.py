import pytest
import requests
import allure
from utils import generate_random_string
from data import COURIER_URL, LOGIN_URL

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.step("Проверяем успешное создание курьера")
    def test_create_courier_success(self, new_courier):
        """
        Тест проверяет успешное создание курьера.
        """
        login_payload = {
            "login": new_courier["login"],
            "password": new_courier["password"]
        }
        login_resp = requests.post(LOGIN_URL, json=login_payload)
        assert login_resp.status_code == 200
        assert "id" in login_resp.json()

    @allure.step("Создаем курьера с уже существующим логином")
    def test_create_same_courier_twice_fails(self):
        """
        Тест проверяет, что создание курьера с уже существующим логином возвращает ошибку.
        """
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }

        response1 = requests.post(COURIER_URL, json=payload)
        assert response1.status_code == 201

        response2 = requests.post(COURIER_URL, json=payload)
        assert response2.status_code == 409

        login_resp = requests.post(LOGIN_URL, json={"login": payload["login"], "password": payload["password"]})
        courier_id = login_resp.json().get("id")
        if courier_id:
            requests.delete(f"{COURIER_URL}/{courier_id}")

    @allure.step("Создаем курьера без обязательных полей")
    @pytest.mark.parametrize("missing_field, expected_message", [
        ("login", "Недостаточно данных для создания учетной записи"),
        ("password", "Недостаточно данных для создания учетной записи")
    ])
    def test_create_courier_missing_fields(self, missing_field, expected_message):
        """
        Тест проверяет, что создание курьера без обязательных полей возвращает конкретную ошибку.
        """
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }
        payload.pop(missing_field)

        response = requests.post(COURIER_URL, json=payload)
        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"

        body = response.json()
        assert "message" in body, "В ответе нет поля 'message'"
        assert body["message"] == expected_message, f"Ожидали сообщение '{expected_message}', получили '{body['message']}'"
