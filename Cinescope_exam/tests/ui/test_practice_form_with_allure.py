from playwright.sync_api import Page
import allure
import pytest
import time
from datetime import datetime
from Cinescope_exam.models.demoqa_page_objects_with_allure import DemoQAPracticeFormPage


@allure.epic("Тестирование UI DemoQA")
@allure.feature("Forms")
@pytest.mark.ui
class TestPracticeForm:
    
    @allure.title("Заполнение и отправка формы Practice Form")
    @allure.description("Тест проверяет заполнение всех полей формы и отправку")
    def test_practice_form(self, page: Page):
        practice_form_page = DemoQAPracticeFormPage(page)
        practice_form_page.open_via_navigation()
        
        with allure.step("Проверка значения даты рождения по умолчанию"):
            today = datetime.now().strftime("%d %b %Y")
            actual_value = page.get_attribute("#dateOfBirthInput", "value")
            assert actual_value == today
        
        practice_form_page.fill_form("Иван", "Иванов", "ivan@test.com", "9876543210", "123 Test Street")
        time.sleep(0.5)
        
        practice_form_page.select_hobbies()
        
        practice_form_page.select_state_and_city("NCR", "Delhi")
        time.sleep(0.5)
        
        with allure.step("Проверка footer"):
            footer_text = page.locator(practice_form_page.footer).text_content()
            assert "TOOLSQA.COM" in footer_text
        
        practice_form_page.submit_form()
        
        with allure.step("Проверка что модальное окно появилось"):
            time.sleep(2)
            modal = page.locator(practice_form_page.modal_content)
            assert modal.is_visible()
        
        with allure.step("Закрытие модального окна"):
            page.locator("#closeLargeModal").click()
            time.sleep(1)
