from playwright.sync_api import Page


def test_example(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.click("text=Elements")
    page.click("text=Text Box")
    page.get_by_role("link", name="Text Box").click()
    page.get_by_role("textbox", name="Full Name").click()
    page.get_by_role("textbox", name="Full Name").fill("qwdqwd")
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("gbbgbg")
    page.get_by_role("textbox", name="Current Address").click()
    page.get_by_role("textbox", name="Current Address").fill("wfweef")
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("gbbgbg@mail.ru")
    page.locator("#permanentAddress").click()
    page.locator("#permanentAddress").fill("tetherherh")
    page.get_by_role("button", name="Submit").click()
