from playwright.sync_api import Page, expect
import time
from datetime import datetime
from Cinescope_exam.models.demoqa_page_objects import DemoQAPracticeFormPage


def test_practice_form(page: Page):
    practice_form_page = DemoQAPracticeFormPage(page)
    practice_form_page.open_via_navigation()

    today = datetime.now().strftime("%d %b %Y")
    actual_value = page.get_attribute("#dateOfBirthInput", "value")
    assert actual_value == today
    
    practice_form_page.enter_first_name("Иван")
    time.sleep(0.5)
    
    practice_form_page.type_last_name("Иванов")
    time.sleep(0.5)
    
    practice_form_page.enter_email("ivan@test.com")
    
    practice_form_page.select_gender_male()
    
    practice_form_page.type_mobile_number("9876543210")
    
    practice_form_page.select_hobby_sports()
    practice_form_page.select_hobby_reading()
    
    practice_form_page.enter_current_address("123 Test Street, Test City")
    
    practice_form_page.select_state("NCR")
    time.sleep(0.5)
    
    practice_form_page.select_city("Delhi")
    time.sleep(0.5)
    
    expected_footer = "© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED."
    expect(page.locator(practice_form_page.footer)).to_have_text(expected_footer)
    
    practice_form_page.click_submit()
    
    time.sleep(2)
    modal = page.locator(".modal-content")
    assert modal.is_visible()
    
    page.locator("#closeLargeModal").click()
    
    time.sleep(1)
