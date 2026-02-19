import pytest
from faker import Faker
from Cinescope_exam.models.base_models import UserResponse

faker = Faker()

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        user_response = UserResponse(**response.json())

        assert user_response.id and user_response.id != '', "ID должен быть не пустым"
        assert user_response.email == creation_user_data.email
        assert user_response.fullName == creation_user_data.fullName
        assert user_response.roles == creation_user_data.roles
        assert user_response.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = UserResponse(**created_user_response.json())
        
        response_by_id = super_admin.api.user_api.get_user(created_user.id)
        user_by_id = UserResponse(**response_by_id.json())
        
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)
        user_by_email = UserResponse(**response_by_email.json())

        assert user_by_id.model_dump() == user_by_email.model_dump(), "Содержание ответов должно быть идентичным"
        assert user_by_id.id and user_by_id.id != '', "ID должен быть не пустым"
        assert user_by_id.email == creation_user_data.email
        assert user_by_id.fullName == creation_user_data.fullName
        assert user_by_id.roles == creation_user_data.roles
        assert user_by_id.verified is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    @pytest.mark.slow
    def test_create_movie_user_role_forbidden(self, common_user, super_admin):
        """
        Негативно-позитивный тест: пользователь с ролью USER не может создать фильм,
        но super_admin может.
        """

        # Подготовка данных для создания фильма с правильными полями
        movie_data = {
            "name": faker.catch_phrase(),
            "description": faker.text(max_nb_chars=200),
            "price": faker.random_int(min=100, max=1000),
            "location": faker.random_element(elements=["MSK", "SPB"]),
            "published": True,
            "genreId": faker.random_int(min=1, max=10)
        }

        # Негативная часть: пользователь с ролью USER пытается создать фильм
        # Ожидаем статус 403 Forbidden
        response_user = common_user.api.movies_api.create_movie(movie_data, expected_status=403)

        assert response_user.status_code == 403, \
            f"Пользователь с ролью USER не должен иметь доступ к созданию фильма. Получен статус: {response_user.status_code}"

        # Позитивная часть: super_admin может создать фильм
        # Ожидаем статус 201 Created
        response_admin = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)

        assert response_admin.status_code == 201, \
            f"Super admin должен иметь доступ к созданию фильма. Получен статус: {response_admin.status_code}"

        # Дополнительная проверка: убеждаемся, что фильм действительно создан
        created_movie = response_admin.json()
        assert created_movie.get('id') and created_movie['id'] != '', "ID фильма должен быть не пустым"
        assert created_movie.get('name') == movie_data['name'], "Название фильма должно совпадать"
        assert created_movie.get('price') == movie_data['price'], "Цена фильма должна совпадать"