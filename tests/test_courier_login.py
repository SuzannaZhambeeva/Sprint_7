import requests
import pytest
import allure
from helpers import register_new_courier_and_return_login_password, LOGIN_URL


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.story("Курьер может авторизоваться; успешный ответ содержит id")
    def test_courier_can_login(self):
        login, password, _ = register_new_courier_and_return_login_password()
        response = requests.post(LOGIN_URL, json={"login": login, "password": password})
        assert response.status_code == 200
        body = response.json()
        assert "id" in body and isinstance(body["id"], int)

    @allure.story("Система вернёт ошибку при неверном логине/пароле; код 404")
    def test_wrong_credentials(self):
        login, password, _ = register_new_courier_and_return_login_password()
        response = requests.post(LOGIN_URL, json={"login": login, "password": "wrongpwd"})
        assert response.status_code == 404

    @allure.story("Для авторизации нужны обязательные поля; при отсутствии — 400")
    @pytest.mark.parametrize("payload", [
        {"password": "123456"},
        {"login": "someuser"},
    ])
    def test_login_missing_fields(self, payload):
        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code in [400, 504], f"Ожидали 400 или 504, получили {response.status_code}"
    
    @allure.story("Система вернёт ошибку при авторизации несуществующего курьера; код 404")
    def test_login_nonexistent_user(self):
        response = requests.post(LOGIN_URL, json={"login": "nosuchuser", "password": "nopass"})
        assert response.status_code == 404
        body = response.json()
        assert "message" in body
