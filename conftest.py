import pytest
import requests
import allure
from data import COURIER_URL, LOGIN_URL
from utils import generate_random_string

@allure.step("Регистрация нового курьера")
def register_new_courier_and_return_login_password():
    """
    Метод регистрации нового курьера
    """
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(COURIER_URL, json=payload)
    if response.status_code == 201:
        login_pass.extend([login, password, first_name])
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
    else:
        allure.attach(str(response.status_code), name="Ошибка регистрации", attachment_type=allure.attachment_type.TEXT)

    return login_pass


@pytest.fixture
def new_courier():
    """
    Фикстура для создания нового курьера перед тестом.
    Возвращает словарь с login, password, firstName.
    После теста курьер удаляется.
    """
    login_pass = register_new_courier_and_return_login_password()
    assert login_pass, "Не удалось создать курьера"

    courier_data = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

    yield courier_data

    with allure.step("Удаляем курьера после теста"):
        login_payload = {"login": courier_data["login"], "password": courier_data["password"]}
        login_resp = requests.post(LOGIN_URL, json=login_payload)
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                del_resp = requests.delete(f"{COURIER_URL}/{courier_id}")
                allure.attach(str(del_resp.status_code), name="Удаление курьера", attachment_type=allure.attachment_type.TEXT)
