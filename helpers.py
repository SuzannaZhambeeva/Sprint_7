import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
COURIER_URL = f"{BASE_URL}/courier"
LOGIN_URL = f"{COURIER_URL}/login"
ORDERS_URL = f"{BASE_URL}/orders"


def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(COURIER_URL, json=payload)

    if response.status_code == 201:
        return login, password, first_name
    return None


def login_and_get_id(login: str, password: str) -> int | None:
    resp = requests.post(LOGIN_URL, json={"login": login, "password": password})
    if resp.status_code == 200 and "id" in resp.json():
        return resp.json()["id"]
    return None


def try_delete_courier(courier_id: int) -> None:
    """Удаление курьера (без падения теста, если не удалось)."""
    try:
        requests.delete(f"{COURIER_URL}/{courier_id}")
    except Exception:
        pass
