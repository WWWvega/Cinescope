import pytest
from faker import Faker

from Cinescope_exam.entities.user import User

faker = Faker()


class TestUser:
    """Тесты для пользователей"""

    def test_create_user(self, super_admin, creation_user_data):
        """Создание пользователя"""
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """Получение пользователя по ID и email"""
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']

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
        admin_data = creation_user_data.copy()
        admin_data['roles'] = ["ADMIN"]

        response = super_admin.api.user_api.create_user(admin_data).json()

        # Этот assert упадет, т.к. API возвращает USER
        assert response.get('roles') == ["ADMIN"], "API должен создать ADMIN"


# USEFIXTURES - класс с автоматической фикстурой
@pytest.mark.usefixtures("super_admin")
class TestUserPermissions:
    """Тесты прав доступа"""

    def test_permissions_check(self):
        """Проверка прав доступа"""
        print("super_admin фикстура загружена автоматически")
        assert True