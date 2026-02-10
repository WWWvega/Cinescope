import pytest
from faker import Faker

from Cinescope_exam.utils.data_generator import DataGenerator

faker = Faker()


class TestMoviesNegative:
    """Негативные тесты для /movies"""

    def test_create_movie_conflict(self, api_manager):
        """POST /movies — проверка ошибки при дублирующемся названии"""
        # создаём фильм
        movie_name = DataGenerator.generate_random_name()
        movie_data = {
            "name": movie_name,
            "price": 200,
            "description": "Описание",
            "imageUrl": "http://example.com/img.jpg",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        response = api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201

        # создаём фильм с тем же названием → ожидаем 409 Conflict
        with pytest.raises(ValueError) as e:
            api_manager.movies_api.create_movie(movie_data)
        assert "409" in str(e.value)

    def test_create_movie_invalid_location(self, api_manager):
        """POST /movies — проверка ошибки при неверном location"""
        movie_data = {
            "name": DataGenerator.generate_random_name(),
            "price": 200,
            "description": "Описание",
            "imageUrl": "http://example.com/img.jpg",
            "location": "NYC",  # неверное значение
            "published": True,
            "genreId": 1
        }
        with pytest.raises(ValueError) as e:
            api_manager.movies_api.create_movie(movie_data)
        assert "400" in str(e.value)

    def test_get_movie_not_found(self, api_manager):
        """GET /movies/{id} — проверка ошибки при несуществующем ID"""
        fake_id = 999999
        with pytest.raises(ValueError) as e:
            api_manager.movies_api.get_movie_by_id(fake_id)
        assert "404" in str(e.value)

    def test_update_movie_not_found(self, api_manager):
        """PATCH /movies/{id} — проверка ошибки при несуществующем ID"""
        fake_id = 999999
        with pytest.raises(ValueError) as e:
            api_manager.movies_api.update_movie(fake_id, {"name": "New Name"})
        assert "404" in str(e.value)

    def test_delete_movie_not_found(self, api_manager):
        """DELETE /movies/{id} — проверка ошибки при несуществующем ID"""
        fake_id = 999999
        with pytest.raises(ValueError) as e:
            api_manager.movies_api.delete_movie(fake_id)
        assert "404" in str(e.value)
