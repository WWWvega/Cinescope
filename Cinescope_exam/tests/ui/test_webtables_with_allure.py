from playwright.sync_api import Page, expect
import allure
import pytest
import time
from Cinescope_exam.models.demoqa_page_objects_with_allure import DemoQAWebTablesPage


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
        
        webtables_page.add_record("Иван", "Иванов", "ivan@test.com", "30", "50000", "QA")
        
        time.sleep(3)
