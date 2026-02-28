from playwright.sync_api import Page, expect
import allure
import pytest
from Cinescope_exam.models.demoqa_page_objects_with_allure import DemoQARadioButtonPage, DemoQACheckBoxPage, DemoQADynamicPropertiesPage


@allure.epic("Тестирование UI DemoQA")
@allure.feature("Elements")
@pytest.mark.ui
class TestDemoQAElements:
    
    @allure.title("Проверка активности радио-кнопок")
    @allure.description("Тест проверяет состояние радио-кнопок Yes, Impressive и No")
    def test_radio_button_activity(self, page: Page):
        radio_button_page = DemoQARadioButtonPage(page)
        radio_button_page.open_via_navigation()
        
        with allure.step("Проверка что Yes и Impressive активны, No неактивен"):
            yes_radio = page.locator(radio_button_page.yes_radio)
            expect(yes_radio).to_be_enabled()
            
            impressive_radio = page.locator(radio_button_page.impressive_radio)
            expect(impressive_radio).to_be_enabled()
            
            no_radio = page.locator(radio_button_page.no_radio)
            expect(no_radio).to_be_disabled()
        
        radio_button_page.click_yes_radio()
        
        with allure.step("Проверка результата после клика на Yes"):
            result_text = page.locator(radio_button_page.result_text)
            expect(result_text).to_be_visible()
            expect(result_text).to_contain_text("Yes")
        
        radio_button_page.click_impressive_radio()
        
        with allure.step("Проверка результата после клика на Impressive"):
            expect(result_text).to_contain_text("Impressive")
    
    @allure.title("Проверка видимости чекбоксов")
    @allure.description("Тест проверяет раскрытие дерева чекбоксов")
    def test_checkbox_visibility(self, page: Page):
        checkbox_page = DemoQACheckBoxPage(page)
        checkbox_page.open()

        with allure.step("Проверка что элемент Home виден"):
            home_element = page.locator(checkbox_page.home_element).first
            expect(home_element).to_be_visible()

        checkbox_page.click_toggle_button()

        with allure.step("Проверка что элемент Desktop стал виден"):
            desktop_element = page.locator(checkbox_page.desktop_element)
            expect(desktop_element).to_be_visible()
    
    @allure.title("Проверка появления динамического элемента")
    @allure.description("Тест проверяет элемент который появляется через 5 секунд")
    def test_dynamic_element_appearance(self, page: Page):
        dynamic_page = DemoQADynamicPropertiesPage(page)
        dynamic_page.open()
        
        with allure.step("Проверка что элемент изначально не виден"):
            dynamic_element = page.locator(dynamic_page.visible_after_element)
            expect(dynamic_element).not_to_be_visible()
        
        dynamic_page.wait_for_visible_after_element(timeout=10000)
        
        with allure.step("Проверка что элемент стал виден"):
            expect(dynamic_element).to_be_visible()
            expect(dynamic_element).to_contain_text("Visible After 5 Seconds")
