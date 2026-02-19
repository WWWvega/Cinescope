from pydantic import BaseModel, EmailStr


class RegistrationUserModel(BaseModel):
    """Модель для регистрации пользователя"""
    email: EmailStr
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[str]