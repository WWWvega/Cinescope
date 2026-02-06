
from faker import Faker
import pytest
import requests
from Cinescope_exam.constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from Cinescope_exam.custom_requester.custom_requester import CustomRequester
from Cinescope_exam.utils.data_generator import DataGenerator
from Cinescope_exam.constants import ADMIN_USERNAME, ADMIN_PASSWORD
from Cinescope_exam.api.api_manager import ApiManager

faker = Faker()

@pytest.fixture(scope="function")  # ← Было "session"
def test_user():
    """Новый пользователь для каждого теста"""
    password = faker.password(length=12)
    full_name = f"{faker.first_name()} {faker.last_name()}"
    return {
        "username": faker.user_name(),
        "email": faker.email(),
        "password": password,
        "passwordRepeat": password,
        "fullName": full_name
    }


@pytest.fixture
def registered_user(api_manager, test_user):
    """
    Регистрирует пользователя через API и возвращает данные с id.
    Если пользователь уже зарегистрирован, возвращает существующий.
    """
    if "id" not in test_user:
        response = api_manager.auth_api.register_user(test_user)
        data = response.json()
        test_user["id"] = data["id"]  # сохраняем ID
    return test_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture
def admin_api(api_manager):
    """
    Авторизация админа и установка токена в заголовки.
    Возвращает api_manager с токеном админа.
    """
    api_manager.auth_api.authenticate((ADMIN_USERNAME, ADMIN_PASSWORD))
    return api_manager
