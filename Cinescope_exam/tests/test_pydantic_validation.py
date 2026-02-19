import pytest
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
