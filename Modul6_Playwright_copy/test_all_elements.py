from playwright.sync_api import Page, expect
import time


def test_radio_button_activity(page: Page):
    page.goto("https://demoqa.com/")
    page.click("text=Elements")
    page.click("text=Radio Button")
    
    yes_radio = page.locator("input#yesRadio")
    expect(yes_radio).to_be_enabled()
    
    impressive_radio = page.locator("input#impressiveRadio")
    expect(impressive_radio).to_be_enabled()
    
    no_radio = page.locator("input#noRadio")
    expect(no_radio).to_be_disabled()
    
    page.locator("label[for='yesRadio']").click()
    result_text = page.locator(".text-success")
    expect(result_text).to_be_visible()
    expect(result_text).to_contain_text("Yes")
    
    page.locator("label[for='impressiveRadio']").click()
    expect(result_text).to_contain_text("Impressive")


def test_checkbox_visibility(page: Page):
    page.goto("https://demoqa.com/checkbox")

    home_element = page.locator("text=Home >> visible=true").first
    expect(home_element).to_be_visible()

    toggle_button = page.locator(".rc-tree-treenode-switcher-close").first
    toggle_button.click()

    desktop_element = page.locator("text=Desktop >> visible=true")
    expect(desktop_element).to_be_visible()


def test_dynamic_element_appearance(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")
    
    dynamic_element = page.locator("#visibleAfter")
    expect(dynamic_element).not_to_be_visible()
    
    page.wait_for_selector("#visibleAfter", state="visible", timeout=10000)
    
    expect(dynamic_element).to_be_visible()
    expect(dynamic_element).to_contain_text("Visible After 5 Seconds")
