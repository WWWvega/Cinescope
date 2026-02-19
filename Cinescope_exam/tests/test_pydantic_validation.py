import pytest
from pydantic import ValidationError
from Cinescope_exam.models.base_models import RegistrationUserModel


class TestPydanticValidation:
    """Тесты валидации Pydantic моделей"""

    def test_validate_test_user(self, test_user):

        print(f"\n Исходные данные test_user:\n{test_user}")

        # Валидация
        user = RegistrationUserModel(**test_user)

        # JSON с exclude_unset=True
        json_output = user.model_dump_json(exclude_unset=True, indent=2)
        print(f"\n test_user JSON (exclude_unset=True):\n{json_output}")

        assert user.email == test_user['email']

    def test_validate_creation_user_data(self, creation_user_data):

        print(f"\n Исходные данные creation_user_data:\n{creation_user_data}")

        # Валидация
        user = RegistrationUserModel(**creation_user_data)

        # JSON БЕЗ exclude_unset
        json_output = user.model_dump_json(indent=2)
        print(f"\n creation_user_data JSON (exclude_unset=False):\n{json_output}")

        assert user.verified == True
        assert user.banned == False

    def test_compare_outputs(self, test_user, creation_user_data):

        user1 = RegistrationUserModel(**test_user)
        json1 = user1.model_dump_json(exclude_unset=True, indent=2)

        user2 = RegistrationUserModel(**creation_user_data)
        json2 = user2.model_dump_json(indent=2)

        print(f"\n test_user (exclude_unset=True):\n{json1}")
        print(f"\n creation_user_data (exclude_unset=False):\n{json2}")

        print(" АНАЛИЗ:")
        print("exclude_unset=True  → Убирает None поля")
        print("exclude_unset=False → Показывает все поля")


class TestCustomValidators:
    """Тесты кастомных валидаторов"""

    def test_valid_email_and_password(self):
        """Успешная валидация - правильный email и пароль"""
        valid_data = {
            "email": "user@example.com",
            "fullName": "John Doe",
            "password": "SecurePass123",
            "passwordRepeat": "SecurePass123",
            "roles": ["USER"]
        }
        
        user = RegistrationUserModel(**valid_data)
        print(f"\nУспешная валидация:\n{user.model_dump_json(indent=2)}")
        
        assert user.email == "user@example.com"
        assert user.password == "SecurePass123"

    def test_invalid_email_without_at(self):
        """Ошибка валидации - email без '@'"""
        invalid_data = {
            "email": "userexample.com",
            "fullName": "John Doe",
            "password": "SecurePass123",
            "passwordRepeat": "SecurePass123",
            "roles": ["USER"]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            RegistrationUserModel(**invalid_data)
        
        print(f"\nОшибка валидации email:\n{exc_info.value}")
        assert "Email должен содержать '@'" in str(exc_info.value)

    def test_invalid_password_too_short(self):
        """Ошибка валидации - пароль меньше 8 символов"""
        invalid_data = {
            "email": "user@example.com",
            "fullName": "John Doe",
            "password": "short",
            "passwordRepeat": "short",
            "roles": ["USER"]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            RegistrationUserModel(**invalid_data)
        
        print(f"\nОшибка валидации пароля:\n{exc_info.value}")
        assert "Пароль должен содержать не меньше 8 символов" in str(exc_info.value)

    def test_multiple_validation_errors(self):
        """Ошибка валидации - несколько ошибок одновременно"""
        invalid_data = {
            "email": "bademail",
            "fullName": "John Doe",
            "password": "123",
            "passwordRepeat": "123",
            "roles": ["USER"]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            RegistrationUserModel(**invalid_data)
        
        error_str = str(exc_info.value)
        print(f"\nМножественные ошибки валидации:\n{exc_info.value}")
        
        assert "Email должен содержать '@'" in error_str
        assert "Пароль должен содержать не меньше 8 символов" in error_str
