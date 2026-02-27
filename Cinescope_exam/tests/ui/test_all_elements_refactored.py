from playwright.sync_api import Page, expect
from Cinescope_exam.models.demoqa_page_objects import DemoQARadioButtonPage, DemoQACheckBoxPage, DemoQADynamicPropertiesPage


def test_radio_button_activity(page: Page):
    radio_button_page = DemoQARadioButtonPage(page)
    radio_button_page.open_via_navigation()
    
    yes_radio = page.locator(radio_button_page.yes_radio)
    expect(yes_radio).to_be_enabled()
    
    impressive_radio = page.locator(radio_button_page.impressive_radio)
    expect(impressive_radio).to_be_enabled()
    
    no_radio = page.locator(radio_button_page.no_radio)
    expect(no_radio).to_be_disabled()
    
    radio_button_page.click_yes_radio()
    result_text = page.locator(radio_button_page.result_text)
    expect(result_text).to_be_visible()
    expect(result_text).to_contain_text('Yes')
    
    radio_button_page.click_impressive_radio()
    expect(result_text).to_contain_text('Impressive')


def test_checkbox_visibility(page: Page):
    checkbox_page = DemoQACheckBoxPage(page)
    checkbox_page.open()

    home_element = page.locator(checkbox_page.home_element).first
    expect(home_element).to_be_visible()

    checkbox_page.click_toggle_button()

    desktop_element = page.locator(checkbox_page.desktop_element)
    expect(desktop_element).to_be_visible()


def test_dynamic_element_appearance(page: Page):
    dynamic_page = DemoQADynamicPropertiesPage(page)
    dynamic_page.open()
    
    dynamic_element = page.locator(dynamic_page.visible_after_element)
    expect(dynamic_element).not_to_be_visible()
    
    dynamic_page.wait_for_visible_after_element(timeout=10000)
    
    expect(dynamic_element).to_be_visible()
    expect(dynamic_element).to_contain_text('Visible After 5 Seconds')
