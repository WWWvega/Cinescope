from pydantic import BaseModel
from typing import Optional
from Cinescope_exam.enums.roles import Roles


class RegistrationUserModel(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None