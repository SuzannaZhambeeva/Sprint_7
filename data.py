BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

COURIER_URL = f"{BASE_URL}/courier"
LOGIN_URL = f"{COURIER_URL}/login"
ORDERS_URL = f"{BASE_URL}/orders"

DEFAULT_ORDER = {
    "firstName": "TestName",
    "lastName": "TestSurname",
    "address": "ул. Тестовая, 1",
    "metroStation": "1",
    "phone": "+79999999999",
    "rentTime": 5,
    "deliveryDate": "2025-08-21",
    "comment": "Тестовый заказ",
}
