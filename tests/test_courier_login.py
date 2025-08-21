import pytest
import requests
import allure
from conftest import generate_random_string
from data import LOGIN_URL


@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.step("Авторизация с корректными данными")
    def test_login_success(self, new_courier):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert isinstance(body["id"], int)

    @allure.step("Авторизация с неверным логином")
    def test_login_wrong_login(self, new_courier):
        payload = {"login": "wrong_login", "password": new_courier["password"]}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.step("Авторизация с неверным паролем")
    def test_login_wrong_password(self, new_courier):
        payload = {"login": new_courier["login"], "password": "wrong_password"}
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.step("Авторизация с пропущенным полем")
    @pytest.mark.parametrize("missing_field, expected_status, expected_message", [
        ("login", 400, "Недостаточно данных для входа"),
        ("password", 504, None),
    ])
    def test_login_missing_field(self, missing_field, expected_status, expected_message):
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string()
        }
        payload.pop(missing_field)
        response = requests.post(LOGIN_URL, json=payload)

        assert response.status_code == expected_status

        if expected_message: 
            assert response.json().get("message") == expected_message
        else: 
            assert response.text != ""  
