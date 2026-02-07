from Cinescope_exam.clients.auth_api import AuthAPI
from Cinescope_exam.clients.user_api import UserAPI
from Cinescope_exam.api.movies_api import MoviesAPI



class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)