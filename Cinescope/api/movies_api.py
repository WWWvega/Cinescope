from typing import Dict, Any, Optional
from custom_requester import CustomRequester


class MoviesAPI:
    def __init__(self):
        self.requester = CustomRequester()

    def get_movies(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        response = self.requester.request("GET", "/movies", params=params)
        return response.json()

    def create_movie(self, movie_data: Dict) -> Dict[str, Any]:
        response = self.requester.request("POST", "/movies", json=movie_data, expected_status=201)
        return response.json()

    def get_movie(self, movie_id: int) -> Dict[str, Any]:
        response = self.requester.request("GET", f"/movies/{movie_id}")
        return response.json()

    def update_movie(self, movie_id: int, movie_data: Dict) -> Dict[str, Any]:
        response = self.requester.request("PUT", f"/movies/{movie_id}", json=movie_data)
        return response.json()

    def delete_movie(self, movie_id: int) -> None:
        self.requester.request("DELETE", f"/movies/{movie_id}", expected_status=204)
