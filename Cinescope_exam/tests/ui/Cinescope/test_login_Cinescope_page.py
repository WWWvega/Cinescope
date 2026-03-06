import allure
import pytest
import time
from Cinescope_exam.models.page_object_models import CinescopLoginPage
from playwright.sync_api import sync_playwright

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
   @allure.title("Проверка сообщения об ошибке при вводе неверных данных")
   def test_login_with_invalid_credentials(self, page):

      login_page = CinescopLoginPage(page)

      login_page.open()
      login_page.login("wrong@email.com", "wrongpassword123")  # Заведомо неверные данные

      login_page.assert_error_message_was_pop_up()  # Проверка появления и исчезновения сообщения об ошибке
      login_page.make_screenshot_and_attach_to_allure()

