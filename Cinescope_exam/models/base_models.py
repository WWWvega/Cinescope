from pydantic import BaseModel, field_validator
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

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        """Проверяем, что email содержит '@'"""
        if "@" not in value:
            raise ValueError("Email должен содержать '@'")
        return value

    @field_validator("password")
    def check_password_length(cls, value: str) -> str:
        """Проверяем, что пароль не меньше 8 символов"""
        if len(value) < 8:
            raise ValueError("Пароль должен содержать не меньше 8 символов")
        return value