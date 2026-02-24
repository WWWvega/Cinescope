import pytest
from faker import Faker

from Cinescope_exam.entities.user import User
from Cinescope_exam.models.base_models import UserResponse

faker = Faker()


class TestUser:
    """Тесты для пользователей"""

    def test_create_user(self, super_admin, creation_user_data):
        """Создание пользователя"""
        response = super_admin.api.user_api.create_user(creation_user_data)
        user_response = UserResponse(**response.json())

        assert user_response.id and user_response.id != '', "ID должен быть не пустым"
        assert user_response.email == creation_user_data.email
        assert user_response.fullName == creation_user_data.fullName
        assert user_response.roles == creation_user_data.roles
        assert user_response.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """Получение пользователя по ID и email"""
        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = UserResponse(**created_user_response.json())
        
        response_by_id = super_admin.api.user_api.get_user(created_user.id)
        user_by_id = UserResponse(**response_by_id.json())
        
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)
        user_by_email = UserResponse(**response_by_email.json())

        assert user_by_id.model_dump() == user_by_email.model_dump(), "Содержание ответов должно быть идентичным"
        assert user_by_id.id and user_by_id.id != '', "ID должен быть не пустым"
        assert user_by_id.email == creation_user_data.email

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        """USER не может получить данные другого пользователя"""
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    # SKIP - тест в разработке
    @pytest.mark.skip(reason="Функционал в разработке")
    def test_update_user(self, super_admin):
        """Обновление пользователя - пока не готово"""
        pass

    # XFAIL - известный баг
    @pytest.mark.xfail(reason="Баг: API создает USER вместо ADMIN")
    def test_create_admin_user(self, super_admin, creation_user_data):
        """Создание пользователя с ролью ADMIN"""
        from Cinescope_exam.models.base_models import TestUser
        from Cinescope_exam.enums.roles import Roles
        
        admin_data = TestUser(
            email=creation_user_data.email,
            fullName=creation_user_data.fullName,
            password=creation_user_data.password,
            passwordRepeat=creation_user_data.passwordRepeat,
            verified=creation_user_data.verified,
            banned=creation_user_data.banned,
            roles=[Roles.ADMIN]
        )

        response = super_admin.api.user_api.create_user(admin_data)
        user_response = UserResponse(**response.json())

        # Этот assert упадет, т.к. API возвращает USER
        assert user_response.roles == [Roles.ADMIN], "API должен создать ADMIN"


# USEFIXTURES - класс с автоматической фикстурой
@pytest.mark.usefixtures("super_admin")
class TestUserPermissions:
    """Тесты прав доступа"""

    def test_permissions_check(self):
        """Проверка прав доступа"""
        print("super_admin фикстура загружена автоматически")
        assert True