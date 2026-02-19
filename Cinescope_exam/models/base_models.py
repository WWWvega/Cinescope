from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from enum import Enum
import datetime
from Cinescope_exam.enums.roles import Roles


class ProductType(str, Enum):
    ELECTRONICS = "Электроника"
    CLOTHING = "Одежда"
    FOOD = "Еда"
    BOOKS = "Книги"


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    product_type: ProductType


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


class TestUser(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value


class UserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str = Field(min_length=1, max_length=100)
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value