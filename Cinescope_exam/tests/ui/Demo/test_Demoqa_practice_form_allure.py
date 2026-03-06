from playwright.sync_api import Page
import allure
import pytest
from datetime import datetime
from Cinescope_exam.models.page_object_models import DemoQAPracticeFormPage
from Cinescope_exam.utils.data_generator import DataGenerator
from faker import Faker
from playwright.sync_api import expect

faker = Faker('ru_RU')

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

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = DataGenerator.generate_random_email()
        phone = DataGenerator.generate_phone_number()
        address = DataGenerator.generate_address()

        practice_form_page.fill_form(first_name, last_name, email, phone, address)

        practice_form_page.select_hobbies()
        
        practice_form_page.select_state_and_city("NCR", "Delhi")

        with allure.step("Проверка footer"):
            footer_text = page.locator(practice_form_page.footer).text_content()
            assert "TOOLSQA.COM" in footer_text
        
        practice_form_page.submit_form()
        
        with allure.step("Проверка что модальное окно появилось"):

            modal = page.locator(practice_form_page.modal_content)

            expect(modal).to_be_visible(timeout=5000)
        
        with allure.step("Закрытие модального окна"):
            page.locator("#closeLargeModal").click()

