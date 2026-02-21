import pytest
import allure
from faker import Faker

from Cinescope_exam.utils.data_generator import DataGenerator
from Cinescope_exam.constants import BASE_URL, API_BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD, LOGIN_ENDPOINT

faker = Faker()


@allure.epic("Cinescope")
@allure.feature("Movies API")
class TestMovies:
    """Тесты для endpoint /movies"""

    @allure.story("Получение списка фильмов")
    @allure.title("GET /movies - Успешное получение списка всех фильмов")
    @allure.description("Проверяем, что API возвращает список фильмов со статусом 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movies(self, api_manager):
        """GET /movies — проверка получения списка фильмов"""
        with allure.step("Отправка GET запроса на /movies"):
            response = api_manager.movies_api.get_movies()
        
        with allure.step("Проверка статус кода 200"):
            assert response.status_code == 200, f"Ошибка: {response.text}"
        
        with allure.step("Проверка наличия ключа 'movies' в ответе"):
            data = response.json()
            assert "movies" in data, "Отсутствует ключ 'movies'"
            allure.attach(str(data), name="Response Data", attachment_type=allure.attachment_type.JSON)

    def test_get_movie_by_id(self, api_manager):
        """GET /movies/{id} — проверка получения фильма по ID"""
        movies = api_manager.movies_api.get_movies().json().get("movies", [])
        if not movies:
            pytest.skip("Нет фильмов для проверки")
        movie_id = movies[0]["id"]
        response = api_manager.movies_api.get_movie_by_id(movie_id)
        assert response.status_code == 200, f"Ошибка: {response.text}"
        movie = response.json()
        assert movie["id"] == movie_id, "ID фильма не совпадает"

    @allure.story("Создание фильма")
    @allure.title("POST /movies - Успешное создание нового фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_movie(self, api_manager):
        """POST /movies — проверка создания фильма"""
        with allure.step("Подготовка данных для создания фильма"):
            movie_data = {
                "name": DataGenerator.generate_random_name(),
                "price": faker.random_int(min=100, max=500),
                "description": faker.paragraph(nb_sentences=3),
                "imageUrl": faker.image_url(),
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
            allure.attach(str(movie_data), name="Movie Data", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Отправка POST запроса на /movies"):
            response = api_manager.movies_api.create_movie(movie_data)
        
        with allure.step("Проверка статус кода 201"):
            assert response.status_code == 201, f"Ошибка: {response.text}"
        
        with allure.step("Проверка соответствия имени фильма"):
            movie = response.json()
            assert movie["name"] == movie_data["name"]
            allure.attach(str(movie), name="Created Movie", attachment_type=allure.attachment_type.JSON)

    def test_update_movie(self, api_manager):
        """PATCH /movies/{id} — проверка обновления фильма"""
        response = api_manager.movies_api.get_movies()
        movies = response.json()["movies"]
        if not movies:
            pytest.skip("Нет фильмов для обновления")
        movie_id = movies[0]["id"]
        new_name = faker.sentence(nb_words=3)
        response = api_manager.movies_api.update_movie(movie_id, {"name": new_name})
        assert response.status_code == 200, f"Ошибка: {response.text}"
        updated_movie = response.json()
        assert updated_movie["name"] == new_name, "Имя фильма не обновилось"

    def test_delete_movie(self, api_manager):
        response = api_manager.movies_api.get_movies()
        movies = response.json()["movies"]
        if not movies:
            pytest.skip("Нет фильмов для удаления")
        movie_id = movies[0]["id"]
        response = api_manager.movies_api.delete_movie(movie_id)
        assert response.status_code == 200, f"Ошибка: {response.text}"
        deleted_movie = response.json()
        assert deleted_movie["id"] == movie_id

    @pytest.mark.parametrize("filters, description", [
        ({"minPrice": 100, "maxPrice": 500}, "Фильтр по минимальной и максимальной цене"),
        pytest.param({"location": "MSK"}, "Фильтр по локации MSK", marks=pytest.mark.xfail(reason="БАГ: API не фильтрует по location")),
        ({"genreId": 1}, "Фильтр по ID жанра 1"),
        ({"genreId": 2}, "Фильтр по ID жанра 2"),
        ({"genreId": 3}, "Фильтр по ID жанра 3"),
        ({"minPrice": 200, "maxPrice": 800}, "Фильтр по минимальной и максимальной цене 200-800"),
        ({"minPrice": 300, "genreId": 1}, "Фильтр по минимальной цене и жанру 1"),
        ({"maxPrice": 1000, "genreId": 3}, "Фильтр по максимальной цене и жанру 3"),
        ({}, "Без фильтров - все фильмы"),
    ])
    def test_get_all_movies_with_filters(self, super_admin, filters, description):

        # Получаем фильмы с заданными фильтрами напрямую через session
        url = f"{API_BASE_URL}movies"
        response = super_admin.api.session.get(url, params=filters)

        assert response.status_code == 200, \
            f"Ошибка при получении фильмов с фильтрами: {description}. Статус: {response.status_code}"

        response_data = response.json()

        # Проверяем, что ответ - это словарь с ключом "movies"
        assert isinstance(response_data, dict), f"Ответ должен быть словарем. Получено: {type(response_data)}"
        assert "movies" in response_data, "В ответе должен быть ключ 'movies'"

        movies = response_data["movies"]

        # Проверяем, что movies - это список
        assert isinstance(movies, list), f"movies должен быть списком. Получено: {type(movies)}"

        # Проверяем фильтры (если есть результаты)
        if movies:
            for movie in movies:
                # Проверка minPrice
                if "minPrice" in filters:
                    assert movie.get("price") >= filters["minPrice"], \
                        f"Цена фильма {movie.get('price')} меньше минимальной {filters['minPrice']}"

                # Проверка maxPrice
                if "maxPrice" in filters:
                    assert movie.get("price") <= filters["maxPrice"], \
                        f"Цена фильма {movie.get('price')} больше максимальной {filters['maxPrice']}"

                # Проверка location
                if "location" in filters:
                    assert movie.get("location") == filters["location"], \
                        f"Локация фильма {movie.get('location')} не совпадает с {filters['location']}"

                # Проверка genreId
                if "genreId" in filters:
                    assert movie.get("genreId") == filters["genreId"], \
                        f"ID жанра {movie.get('genreId')} не совпадает с {filters['genreId']}"

    @allure.story("Авторизация и права доступа")
    @allure.title("DELETE /movies/{id} - SUPER_ADMIN может удалить фильм")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movie_super_admin(self, super_admin):
        """DELETE /movies/{id} — SUPER_ADMIN может удалить фильм"""
        with allure.step("Создание тестового фильма"):
            movie_data = {
                "name": faker.catch_phrase(),
                "price": 500,
                "description": faker.text(),
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
            allure.attach(str(movie_data), name="Movie Data", attachment_type=allure.attachment_type.JSON)
            created_movie = super_admin.api.movies_api.create_movie(movie_data).json()
            movie_id = created_movie["id"]
            allure.attach(str(movie_id), name="Created Movie ID", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Удаление фильма ID={movie_id} от SUPER_ADMIN"):
            url = f"{API_BASE_URL}movies/{movie_id}"
            response = super_admin.api.session.delete(url)

        with allure.step("Проверка успешного удаления (статус 200)"):
            assert response.status_code == 200, f"SUPER_ADMIN должен мочь удалить фильм. Статус: {response.status_code}"

    @pytest.mark.slow
    def test_delete_movie_admin(self, super_admin, admin_user):
        # Создаем фильм от super_admin
        movie_data = {
            "name": faker.catch_phrase(),
            "price": 500,
            "description": faker.text(),
            "location": "MSK",
            "published": True,
            "genreId": 1
        }

        created_movie = super_admin.api.movies_api.create_movie(movie_data).json()
        movie_id = created_movie["id"]

        # Пытаемся удалить от admin
        url = f"{API_BASE_URL}movies/{movie_id}"
        print(f"\n🔍 DELETE REQUEST: {url}")
        print(f"🔍 USER ROLE: {admin_user.roles}")
        response = admin_user.api.session.delete(url)
        print(f"🔍 DELETE RESPONSE STATUS: {response.status_code}")

        assert response.status_code == 403, f"ADMIN НЕ должен мочь удалить фильм. Статус: {response.status_code}"

        # Cleanup
        super_admin.api.session.delete(url)

    @pytest.mark.slow
    def test_delete_movie_common_user(self, super_admin, common_user):
        """DELETE /movies/{id} — USER НЕ может удалить фильм"""
        # Создаем фильм от super_admin
        movie_data = {
            "name": faker.catch_phrase(),
            "price": 500,
            "description": faker.text(),
            "location": "MSK",
            "published": True,
            "genreId": 1
        }

        created_movie = super_admin.api.movies_api.create_movie(movie_data).json()
        movie_id = created_movie["id"]

        # Пытаемся удалить от common_user
        url = f"{API_BASE_URL}movies/{movie_id}"
        response = common_user.api.session.delete(url)
        print(f"🔍 DELETE RESPONSE STATUS: {response.status_code}")

        assert response.status_code == 403, f"USER НЕ должен мочь удалить фильм. Статус: {response.status_code}"

        # Cleanup
        super_admin.api.session.delete(url)