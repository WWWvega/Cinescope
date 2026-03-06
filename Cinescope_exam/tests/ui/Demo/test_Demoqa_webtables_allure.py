from playwright.sync_api import Page, expect
import allure
import pytest
import time
from Cinescope_exam.models.page_object_models import DemoQAWebTablesPage
from Cinescope_exam.utils.data_generator import DataGenerator
import random
from faker import Faker
faker = Faker('ru_RU')

@allure.epic("Тестирование UI DemoQA")
@allure.feature("Web Tables")
@pytest.mark.ui
class TestWebTables:
    
    @allure.title("Добавление записи в таблицу")
    @allure.description("Тест проверяет добавление новой записи в Web Tables")
    def test_webtables_add_record(self, page: Page):
        webtables_page = DemoQAWebTablesPage(page)
        webtables_page.open_via_navigation()
        
        webtables_page.click_add_button()
        
        with allure.step("Проверка что модальная форма появилась"):
            modal_form = page.locator(webtables_page.modal_form)
            expect(modal_form).to_be_visible()

        test_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": DataGenerator.generate_random_email(),
            "age": str(random.randint(18, 65)),
            "salary": str(random.randint(30000, 150000)),
            "department": random.choice(["QA", "Dev", "Marketing", "Sales"])
        }

        allure.attach(str(test_data), "Тестовые данные", allure.attachment_type.TEXT)

        webtables_page.add_record(
            test_data["first_name"],
            test_data["last_name"],
            test_data["email"],
            test_data["age"],
            test_data["salary"],
            test_data["department"]
        )

        with allure.step("Проверка что модальное окно закрылось"):
            expect(modal_form).not_to_be_visible(timeout=5000)

        with allure.step("Проверка что запись добавлена в таблицу"):
            table_row = page.locator(f"text={test_data['email']}")
            expect(table_row).to_be_visible()

