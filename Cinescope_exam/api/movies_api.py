from typing import Dict, Any

import requests

from Cinescope_exam.constants import API_BASE_URL
from Cinescope_exam.custom_requester.custom_requester import CustomRequester


class MoviesAPI:
    def __init__(self, session):
        self.requester = CustomRequester(session=session, base_url=API_BASE_URL)

    def get_movies(self) -> requests.Response:
        response = self.requester.send_request("GET", "/movies")
        return response

    def create_movie(self, movie_data: Dict[str, Any], expected_status=201) -> requests.Response:
        response = self.requester.send_request("POST", "/movies", data=movie_data, expected_status=expected_status)
        return response

    def get_movie_by_id(self, movie_id: int, expected_status=200) -> requests.Response:
        response = self.requester.send_request("GET", f"/movies/{movie_id}", expected_status=expected_status)
        return response

    def update_movie(self, movie_id: int, movie_data: Dict[str, Any], expected_status=200) -> requests.Response:
        response = self.requester.send_request("PATCH", f"/movies/{movie_id}", data=movie_data, expected_status=expected_status)
        return response

    def delete_movie(self, movie_id: int, expected_status=200) -> requests.Response:
        response = self.requester.send_request("DELETE", f"/movies/{movie_id}", expected_status=expected_status)
        return response
