from typing import Dict, Any, Optional
from Cinescope_exam.custom_requester.custom_requester import CustomRequester
from Cinescope_exam.constants import API_BASE_URL

class MoviesAPI:
    def __init__(self, session):
        self.requester = CustomRequester(session=session, base_url=API_BASE_URL)

    def get_movies(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        response = self.requester.send_request("GET", "/movies")
        return response

    def create_movie(self, movie_data: Dict) -> Dict[str, Any]:
        response = self.requester.send_request("POST", "/movies", json=movie_data, expected_status=201)
        return response

    def get_movie(self, movie_id: int) -> Dict[str, Any]:
        response = self.requester.send_request("GET", f"/movies/{movie_id}")
        return response

    def update_movie(self, movie_id: int, movie_data: Dict) -> Dict[str, Any]:
        response = self.requester.send_request("PATCH", f"/movies/{movie_id}", json=movie_data)
        return response

    def delete_movie(self, movie_id: int) -> None:
        self.requester.send_request("DELETE", f"/movies/{movie_id}", expected_status=204)
