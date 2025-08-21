import pytest
import requests
import allure
from data import COURIER_URL, LOGIN_URL
from utils import generate_random_string


def register_new_courier_and_return_login_password():
    """
    Метод регистрации нового курьера.
    Возвращает словарь с login, password, firstName.
    В случае ошибки бросает исключение.
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    with allure.step("Регистрируем нового курьера"):
        response = requests.post(COURIER_URL, json=payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.status_code) + " " + str(response.text), name="Response", attachment_type=allure.attachment_type.JSON)

        if response.status_code != 201:
            raise Exception(f"Не удалось создать курьера: {response.status_code} {response.text}")

    return {"login": login, "password": password, "firstName": first_name}


@pytest.fixture
def new_courier():
    """
    Фикстура для создания нового курьера перед тестом.
    Возвращает словарь с login, password, firstName.
    После теста курьер удаляется.
    """
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data

    # Удаление курьера после теста
    with allure.step("Удаляем курьера после теста"):
        login_payload = {"login": courier_data["login"], "password": courier_data["password"]}
        login_resp = requests.post(LOGIN_URL, json=login_payload)
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                del_resp = requests.delete(f"{COURIER_URL}/{courier_id}")
                allure.attach(str(del_resp.status_code), name="Удаление курьера", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(str(login_resp.status_code), name="Ошибка при логине для удаления курьера", attachment_type=allure.attachment_type.TEXT)
