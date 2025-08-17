import pytest
import requests
import sys, os
sys.path.append(os.path.dirname(__file__))

@pytest.fixture
def new_courier():
    creds = register_new_courier_and_return_login_password()
    assert creds, "Не удалось создать нового курьера"
    login, password, first_name = creds
    yield {"login": login, "password": password, "firstName": first_name}

@pytest.fixture
def courier_id(new_courier):
    payload = {"login": new_courier["login"], "password": new_courier["password"]}
    response = requests.post(f"{COURIER_URL}/login", json=payload)
    assert response.status_code == 200, f"Не удалось авторизовать курьера, статус {response.status_code}"
    body = response.json()
    assert "id" in body, "В ответе нет id курьера"
    return body["id"]

@pytest.fixture
def test_order():
    def _create_order(colors=None):
        order = {
            "firstName": "Ivan",
            "lastName": "Ivanov",
            "address": "Moscow, Red Square, 1",
            "metroStation": 1,
            "phone": "+79999999999",
            "rentTime": 5,
            "deliveryDate": "2025-08-20",
            "comment": "Test order",
            "color": colors or []
        }
        response = requests.post(ORDER_URL, json=order)
        assert response.status_code == 201, f"Не удалось создать заказ, статус {response.status_code}"
        body = response.json()
        assert "track" in body, "В ответе нет track"
        return body
    return _create_order

@pytest.fixture
def delete_courier_after_test():
    created_ids = []

    yield created_ids

    for courier_id in created_ids:
        requests.delete(f"{COURIER_URL}/{courier_id}")
