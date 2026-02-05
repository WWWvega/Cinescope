import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def patch_data():
    return {
        "firstname": "PATCHED_Name",
        "totalprice": 999
    }

# ✅ НЕгативные fixtures для разных сценариев
@pytest.fixture
def invalid_missing_fields():
    """POST: отсутствуют обязательные поля"""
    return {
        "lastname": "Smith",  # ❌ Нет firstname
        "totalprice": 100
    }

@pytest.fixture
def invalid_price_string():
    """POST/PUT: totalprice как строка"""
    return {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": "сто рублей",  # ❌ Строка вместо числа
        "depositpaid": True,
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def invalid_empty_data():
    """POST/PUT/PATCH: пустые данные"""
    return {}

@pytest.fixture
def invalid_booking_dates():
    """Некорректные bookingdates"""
    return {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "invalid-date",  # ❌ Неверный формат
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def nonexistent_booking_id():
    """ID который точно не существует"""
    return 999999