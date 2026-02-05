"""Тесты эндпоинта /movies для экзамена Модуль 4."""
import pytest
import requests
from src.movies_api import MoviesApi
from src.custom_requester import CustomRequester
from src.data_generator import DataGenerator
from constants import BASE_URL, MOVIES_ENDPOINT


@pytest.fixture(scope="function")
def movies_api() -> MoviesApi:
    """Фикстура MoviesApi — обязательна по ТЗ экзамена."""
    requester = CustomRequester()
    api = MoviesApi(requester=requester)
    yield api
    api.requester.session.close()


class TestMoviesAPI:
    """Тесты GET /movies — основа экзамена."""

    @pytest.mark.parametrize("genre", DataGenerator.get_all_valid_genres())
    def test_get_movies_by_valid_genre_positive(self, movies_api, genre):
        """
        ✅ ПОЗИТИВНЫЙ тест: фильтр по валидному жанру.
        Атомарный, стабильный, без хардкода.
        """
        response_data = movies_api.get_movies_by_genre(genre)

        movies = response_data.get("movies", [])
        assert len(movies) > 0, f"Ожидали фильмы жанра '{genre}', получили пустой список"

        # Проверяем ВСЕ фильмы имеют нужный жанр
        for movie in movies:
            assert genre.lower() in movie["genre"].lower(), \
                f"Фильм '{movie['title']}' не содержит жанр '{genre}'"

    @pytest.mark.parametrize("invalid_genre", DataGenerator.get_all_invalid_genres())
    def test_get_movies_by_invalid_genre_negative(self, movies_api, invalid_genre):
        """
        ❌ НЕГАТИВНЫЙ тест: невалидные жанры возвращают пустой список.
        """
        response_data = movies_api.get_movies_by_genre(invalid_genre)

        movies = response_data.get("movies", [])
        assert movies == [], \
            f"Невалидный жанр '{invalid_genre}' вернул фильмы: {len(movies)}"

    def test_movies_pagination_first_page(self, movies_api):
        """📄 Тест пагинации — первая страница."""
        response_data = movies_api.get_movies_paginated(page=1, limit=5)

        assert response_data.get("page") == 1
        assert len(response_data.get("movies", [])) <= 5
        assert "total_pages" in response_data

    def test_movies_random_genre_filter(self, movies_api):
        """
        🔄 Тест с рандомными данными — демонстрирует DataGenerator.
        """
        genre = DataGenerator.generate_random_movie_genre()
        response_data = movies_api.get_movies_by_genre(genre)

        movies = response_data.get("movies", [])
        assert len(movies) > 0
        for movie in movies:
            assert genre.lower() in movie["genre"].lower()

    @pytest.mark.critical
    def test_popular_movies_critical_path(self, movies_api):
        """
        🎖️ КРИТИЧЕСКИЙ путь — топ популярных фильмов.
        """
        response_data = movies_api.get_popular_movies(limit=10)

        movies = response_data.get("movies", [])
        assert len(movies) >= 3
        assert all("title" in movie for movie in movies)

    def test_movies_api_stability(self, movies_api):
        """🔄 Стабильность API — несколько запросов подряд."""
        for _ in range(3):
            data = movies_api.get_movies()
            assert data.get("movies")
