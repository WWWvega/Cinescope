from faker import Faker
faker = Faker()

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

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