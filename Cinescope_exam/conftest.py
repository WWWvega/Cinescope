import pytest
import requests
from faker import Faker

from Cinescope_exam.api.api_manager import ApiManager
from Cinescope_exam.constants import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD, LOGIN_ENDPOINT
from Cinescope_exam.custom_requester.custom_requester import CustomRequester
from Cinescope_exam.entities.user import User
from Cinescope_exam.enums.roles import Roles
from Cinescope_exam.resources.user_creds import SuperAdminCreds
from Cinescope_exam.utils.data_generator import DataGenerator

faker = Faker()


@pytest.fixture
def test_user():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
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
    resp = session.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json={
        "email": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    })
    print("LOGIN RESPONSE:", resp.json())
    assert resp.status_code == 200, f"Ошибка логина: {resp.text}"
    token = resp.json().get("accessToken") or resp.json().get("token") or resp.json().get("access_token")
    if not token:
        raise ValueError(f"Токен не найден! Ответ: {resp.json()}")
    session.headers.update({"Authorization": f"Bearer {token}"})
    return ApiManager(session)


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    valid_password = DataGenerator.generate_random_password()
    updated_data.update({
        "password": valid_password,
        "passwordRepeat": valid_password,
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "verified": True,
        "banned": False,
        "roles": ["USER"]
    })
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()


    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user