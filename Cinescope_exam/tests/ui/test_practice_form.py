from playwright.sync_api import Page, expect
import time
from datetime import datetime


def test_practice_form(page: Page):
    page.goto("https://demoqa.com/")
    page.click("text=Forms")
    page.click("text=Practice Form")

    today = datetime.now().strftime("%d %b %Y")
    actual_value = page.get_attribute("#dateOfBirthInput", "value")
    assert actual_value == today
    
    page.locator("#firstName").fill("Иван")
    time.sleep(0.5)
    
    page.locator("#lastName").type("Иванов")
    time.sleep(0.5)
    
    page.locator("#userEmail").fill("ivan@test.com")
    
    page.locator("label[for='gender-radio-1']").click()
    
    page.locator("#userNumber").type("9876543210")
    
    page.locator("#dateOfBirthInput").click()
    time.sleep(0.5)
    page.keyboard.press("Escape")
    
    subjects_input = page.locator("#subjectsInput")
    subjects_input.type("Math")
    time.sleep(0.5)
    page.keyboard.press("Enter")
    
    page.locator("label[for='hobbies-checkbox-1']").click()
    page.locator("label[for='hobbies-checkbox-2']").click()
    
    page.locator("#currentAddress").fill("123 Test Street, Test City")
    
    page.locator("#state").click()
    time.sleep(0.5)
    page.locator("text=NCR").click()
    
    page.locator("#city").click()
    time.sleep(0.5)
    page.locator("text=Delhi").click()
    
    footer = page.locator("footer")
    expected_footer = "© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED."
    expect(footer).to_have_text(expected_footer)
    
    page.locator("#submit").click()
    
    time.sleep(2)
    modal = page.locator(".modal-content")
    assert modal.is_visible()
    
    time.sleep(3)
