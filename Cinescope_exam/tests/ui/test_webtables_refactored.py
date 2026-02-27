from playwright.sync_api import Page, expect
import time
from Cinescope_exam.models.demoqa_page_objects import DemoQAWebTablesPage


def test_webtables_add_record(page: Page):
    webtables_page = DemoQAWebTablesPage(page)
    webtables_page.open_via_navigation()
    
    webtables_page.click_add_button()
    
    modal_form = page.locator(webtables_page.modal_form)
    expect(modal_form).to_be_visible()
    
    webtables_page.enter_first_name("Иван")
    webtables_page.enter_last_name("Иванов")
    webtables_page.enter_email("ivan@test.com")
    webtables_page.enter_age("30")
    webtables_page.enter_salary("50000")
    webtables_page.enter_department("QA")
    
    webtables_page.click_submit()
    
    time.sleep(3)
