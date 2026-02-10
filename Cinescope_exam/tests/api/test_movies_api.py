import pytest
from faker import Faker

from Cinescope_exam.utils.data_generator import DataGenerator

faker = Faker()


class TestMovies:
    """Тесты для endpoint /movies"""

    def test_get_movies(self, api_manager):
        """GET /movies — проверка получения списка фильмов"""
        response = api_manager.movies_api.get_movies()
        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert "movies" in data, "Отсутствует ключ 'movies'"

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

    def test_create_movie(self, api_manager):
        """POST /movies — проверка создания фильма"""
        movie_data = {
            "name": DataGenerator.generate_random_name(),
            "price": faker.random_int(min=100, max=500),
            "description": faker.paragraph(nb_sentences=3),
            "imageUrl": faker.image_url(),
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        response = api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201, f"Ошибка: {response.text}"
        movie = response.json()
        assert movie["name"] == movie_data["name"]

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
