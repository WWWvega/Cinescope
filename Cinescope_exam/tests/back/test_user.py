import pytest
import allure
from faker import Faker
from Cinescope_exam.models.base_models import UserResponse

faker = Faker()

@allure.epic("Cinescope")
@allure.feature("User API")
class TestUser:

    @allure.story("Создание пользователя")
    @allure.title("Успешное создание нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, super_admin, creation_user_data):
        with allure.step("Создание пользователя через API"):
            response = super_admin.api.user_api.create_user(creation_user_data)
            user_response = UserResponse(**response.json())
            allure.attach(str(creation_user_data), name="User Creation Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ID пользователя"):
            assert user_response.id and user_response.id != '', "ID должен быть не пустым"
        
        with allure.step("Проверка корректности данных пользователя"):
            assert user_response.email == creation_user_data.email
            assert user_response.fullName == creation_user_data.fullName
            assert user_response.roles == creation_user_data.roles
            assert user_response.verified is True
            allure.attach(str(user_response.model_dump()), name="Created User Response", attachment_type=allure.attachment_type.JSON)

    @allure.story("Получение пользователя")
    @allure.title("Получение пользователя по ID и Email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создание тестового пользователя"):
            created_user_response = super_admin.api.user_api.create_user(creation_user_data)
            created_user = UserResponse(**created_user_response.json())
            allure.attach(str(created_user.id), name="Created User ID", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step(f"Получение пользователя по ID: {created_user.id}"):
            response_by_id = super_admin.api.user_api.get_user(created_user.id)
            user_by_id = UserResponse(**response_by_id.json())
        
        with allure.step(f"Получение пользователя по Email: {creation_user_data.email}"):
            response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)
            user_by_email = UserResponse(**response_by_email.json())

        with allure.step("Проверка идентичности данных при получении по ID и Email"):
            assert user_by_id.model_dump() == user_by_email.model_dump(), "Содержание ответов должно быть идентичным"
            assert user_by_id.id and user_by_id.id != '', "ID должен быть не пустым"
            assert user_by_id.email == creation_user_data.email
            assert user_by_id.fullName == creation_user_data.fullName
            assert user_by_id.roles == creation_user_data.roles
            assert user_by_id.verified is True
            allure.attach(str(user_by_id.model_dump()), name="User Data", attachment_type=allure.attachment_type.JSON)

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    @allure.story("Авторизация и права доступа")
    @allure.title("USER не может создать фильм, SUPER_ADMIN может")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.slow
    def test_create_movie_user_role_forbidden(self, common_user, super_admin):
        """
        Негативно-позитивный тест: пользователь с ролью USER не может создать фильм,
        но super_admin может.
        """

        with allure.step("Подготовка данных для создания фильма"):
            movie_data = {
                "name": faker.catch_phrase(),
                "description": faker.text(max_nb_chars=200),
                "price": faker.random_int(min=100, max=1000),
                "location": faker.random_element(elements=["MSK", "SPB"]),
                "published": True,
                "genreId": faker.random_int(min=1, max=10)
            }
            allure.attach(str(movie_data), name="Movie Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Негативная проверка: USER пытается создать фильм"):
            response_user = common_user.api.movies_api.create_movie(movie_data, expected_status=403)
            assert response_user.status_code == 403, \
                f"Пользователь с ролью USER не должен иметь доступ к созданию фильма. Получен статус: {response_user.status_code}"
            allure.attach(f"Status: {response_user.status_code}", name="User Response Status", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Позитивная проверка: SUPER_ADMIN создает фильм"):
            response_admin = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)
            assert response_admin.status_code == 201, \
                f"Super admin должен иметь доступ к созданию фильма. Получен статус: {response_admin.status_code}"

        with allure.step("Проверка корректности созданного фильма"):
            created_movie = response_admin.json()
            assert created_movie.get('id') and created_movie['id'] != '', "ID фильма должен быть не пустым"
            assert created_movie.get('name') == movie_data['name'], "Название фильма должно совпадать"
            assert created_movie.get('price') == movie_data['price'], "Цена фильма должна совпадать"
            allure.attach(str(created_movie), name="Created Movie", attachment_type=allure.attachment_type.JSON)