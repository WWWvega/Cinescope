import pytest
from movies_api import MoviesAPI
from data_generator import DataGenerator


class TestMoviesAPI:
    def test_get_movies_list(self, movies_api):
        """GET /movies"""
        response = movies_api.get_movies()
        assert "results" in response

    def test_get_movies_filter(self, movies_api):
        """GET /movies - ФИЛЬТРЫ (ОБЯЗАТЕЛЬНО!)"""
        response = movies_api.get_movies(params={"is_active": True})
        for movie in response["results"]:
            assert movie["is_active"] is True

    def test_create_movie(self, movies_api):
        """POST /movies"""
        movie_data = DataGenerator.movie()
        movie = movies_api.create_movie(movie_data)
        assert movie["title"] == movie_data["title"]


class TestMoviesCRUD:
    def test_get_movie_by_id(self, create_movie_fixture, movies_api):
        """GET /movies/{id}"""
        movie = movies_api.get_movie(create_movie_fixture["id"])
        assert movie["id"] == create_movie_fixture["id"]

    def test_update_movie(self, create_movie_fixture, movies_api):
        """PUT /movies/{id}"""
        new_title = "Обновленный: " + create_movie_fixture["title"]
        updated = movies_api.update_movie(create_movie_fixture["id"], {"title": new_title})
        assert updated["title"] == new_title


def test_negative_no_title(movies_api):
    """Негатив: без title"""
    data = DataGenerator.movie()
    data["title"] = ""
    movies_api.requester.request("POST", "/movies", json=data, expected_status=400)
