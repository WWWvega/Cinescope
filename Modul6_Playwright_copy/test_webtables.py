from playwright.sync_api import Page, expect
import time


def test_webtables_add_record(page: Page):
    page.goto("https://demoqa.com/", timeout=60000)
    page.click("text=Elements", timeout=60000)
    page.click("text=Web Tables", timeout=60000)
    
    add_button = page.locator("button:has-text('Add')")
    add_button.click()
    
    modal_form = page.locator(".modal-content:has-text('Registration Form')")
    expect(modal_form).to_be_visible()
    
    first_name_input = page.locator("input[placeholder='First Name']")
    first_name_input.fill("Иван")
    
    page.locator("input[placeholder='Last Name']").fill("Иванов")
    page.locator("input[placeholder='name@example.com']").fill("ivan@test.com")
    page.locator("input[placeholder='Age']").fill("30")
    page.locator("input[placeholder='Salary']").fill("50000")
    page.locator("input[placeholder='Department']").fill("QA")
    
    submit_button = page.locator("button#submit")
    submit_button.click()
    
    time.sleep(3)
