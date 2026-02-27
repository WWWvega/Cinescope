from playwright.sync_api import Page


class DemoQABasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://demoqa.com/"
        
    def open(self):
        self.page.goto(self.base_url)
        
    def navigate_to_section(self, section_name: str):
        self.page.click(f"text={section_name}")


class DemoQAElementsPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}elements"
        
    def navigate_to_submenu(self, submenu_name: str):
        self.page.click(f"text={submenu_name}")


class DemoQARadioButtonPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}radio-button"
        
        self.yes_radio = "input#yesRadio"
        self.impressive_radio = "input#impressiveRadio"
        self.no_radio = "input#noRadio"
        self.yes_radio_label = "label[for='yesRadio']"
        self.impressive_radio_label = "label[for='impressiveRadio']"
        self.result_text = ".text-success"
        
    def open(self):
        self.page.goto(self.url)
        
    def open_via_navigation(self):
        super().open()
        self.page.click("text=Elements")
        self.page.click("text=Radio Button")
        
    def is_yes_radio_enabled(self) -> bool:
        return self.page.locator(self.yes_radio).is_enabled()
        
    def is_impressive_radio_enabled(self) -> bool:
        return self.page.locator(self.impressive_radio).is_enabled()
        
    def is_no_radio_disabled(self) -> bool:
        return self.page.locator(self.no_radio).is_disabled()
        
    def click_yes_radio(self):
        self.page.locator(self.yes_radio_label).click()
        
    def click_impressive_radio(self):
        self.page.locator(self.impressive_radio_label).click()
        
    def get_result_text(self) -> str:
        return self.page.locator(self.result_text).text_content()
        
    def is_result_visible(self) -> bool:
        return self.page.locator(self.result_text).is_visible()


class DemoQACheckBoxPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}checkbox"
        
        self.home_element = "text=Home >> visible=true"
        self.toggle_button = ".rc-tree-switcher"
        self.desktop_element = "text=Desktop >> visible=true"
        
    def open(self):
        self.page.goto(self.url)
        
    def is_home_visible(self) -> bool:
        return self.page.locator(self.home_element).first.is_visible()
        
    def click_toggle_button(self):
        self.page.locator(self.toggle_button).first.click()
        
    def is_desktop_visible(self) -> bool:
        return self.page.locator(self.desktop_element).is_visible()


class DemoQADynamicPropertiesPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}dynamic-properties"
        
        self.visible_after_element = "#visibleAfter"
        
    def open(self):
        self.page.goto(self.url)
        
    def is_visible_after_element_visible(self) -> bool:
        return self.page.locator(self.visible_after_element).is_visible()
        
    def wait_for_visible_after_element(self, timeout: int = 10000):
        self.page.wait_for_selector(self.visible_after_element, state="visible", timeout=timeout)
        
    def get_visible_after_text(self) -> str:
        return self.page.locator(self.visible_after_element).text_content()


class DemoQATextBoxPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}text-box"
        
        self.full_name_input = "input#userName"
        self.email_input = "input#userEmail"
        self.current_address_input = "textarea#currentAddress"
        self.permanent_address_input = "textarea#permanentAddress"
        self.submit_button = "button#submit"
        
    def open(self):
        self.page.goto(self.url)
        
    def open_via_navigation(self):
        super().open()
        self.page.click("text=Elements")
        self.page.click("text=Text Box")
        
    def enter_full_name(self, name: str):
        self.page.fill(self.full_name_input, name)
        
    def enter_email(self, email: str):
        self.page.fill(self.email_input, email)
        
    def enter_current_address(self, address: str):
        self.page.fill(self.current_address_input, address)
        
    def enter_permanent_address(self, address: str):
        self.page.fill(self.permanent_address_input, address)
        
    def click_submit(self):
        self.page.click(self.submit_button)
        
    def fill_form(self, full_name: str, email: str, current_address: str, permanent_address: str):
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_current_address(current_address)
        self.enter_permanent_address(permanent_address)
        self.click_submit()


class DemoQAPracticeFormPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}automation-practice-form"
        
        self.first_name_input = "#firstName"
        self.last_name_input = "#lastName"
        self.email_input = "#userEmail"
        self.gender_male_label = "label[for='gender-radio-1']"
        self.gender_female_label = "label[for='gender-radio-2']"
        self.gender_other_label = "label[for='gender-radio-3']"
        self.mobile_input = "#userNumber"
        self.date_of_birth_input = "#dateOfBirthInput"
        self.subjects_input = "#subjectsInput"
        self.hobbies_sports_label = "label[for='hobbies-checkbox-1']"
        self.hobbies_reading_label = "label[for='hobbies-checkbox-2']"
        self.hobbies_music_label = "label[for='hobbies-checkbox-3']"
        self.current_address_input = "#currentAddress"
        self.state_dropdown = "#state"
        self.city_dropdown = "#city"
        self.submit_button = "#submit"
        self.footer = "footer"
        self.modal_content = ".modal-content"
        
    def open(self):
        self.page.goto(self.url)
        
    def open_via_navigation(self):
        super().open()
        self.page.click("text=Forms")
        self.page.click("text=Practice Form")
        
    def get_date_of_birth_value(self) -> str:
        return self.page.get_attribute(self.date_of_birth_input, "value")
        
    def enter_first_name(self, name: str):
        self.page.locator(self.first_name_input).fill(name)
        
    def type_last_name(self, name: str):
        self.page.locator(self.last_name_input).type(name)
        
    def enter_email(self, email: str):
        self.page.locator(self.email_input).fill(email)
        
    def select_gender_male(self):
        self.page.locator(self.gender_male_label).click()
        
    def select_gender_female(self):
        self.page.locator(self.gender_female_label).click()
        
    def select_gender_other(self):
        self.page.locator(self.gender_other_label).click()
        
    def type_mobile_number(self, number: str):
        self.page.locator(self.mobile_input).type(number)
        
    def click_date_of_birth(self):
        self.page.locator(self.date_of_birth_input).click()
        
    def close_date_picker(self):
        self.page.keyboard.press("Escape")
        
    def add_subject(self, subject: str):
        self.page.locator(self.subjects_input).type(subject)
        self.page.keyboard.press("Enter")
        
    def select_hobby_sports(self):
        self.page.locator(self.hobbies_sports_label).click()
        
    def select_hobby_reading(self):
        self.page.locator(self.hobbies_reading_label).click()
        
    def select_hobby_music(self):
        self.page.locator(self.hobbies_music_label).click()
        
    def enter_current_address(self, address: str):
        self.page.locator(self.current_address_input).fill(address)
        
    def select_state(self, state: str):
        self.page.locator(self.state_dropdown).click()
        self.page.locator(f"text={state}").click()
        
    def select_city(self, city: str):
        self.page.locator(self.city_dropdown).click()
        self.page.locator(f"text={city}").click()
        
    def get_footer_text(self) -> str:
        return self.page.locator(self.footer).text_content()
        
    def click_submit(self):
        self.page.locator(self.submit_button).click()
        
    def is_modal_visible(self) -> bool:
        return self.page.locator(self.modal_content).is_visible()


class DemoQAWebTablesPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}webtables"
        
        self.add_button = "button:has-text('Add')"
        self.modal_form = ".modal-content:has-text('Registration Form')"
        self.first_name_input = "input[placeholder='First Name']"
        self.last_name_input = "input[placeholder='Last Name']"
        self.email_input = "input[placeholder='name@example.com']"
        self.age_input = "input[placeholder='Age']"
        self.salary_input = "input[placeholder='Salary']"
        self.department_input = "input[placeholder='Department']"
        self.submit_button = "button#submit"
        
    def open(self):
        self.page.goto(self.url)
        
    def open_via_navigation(self):
        super().open()
        self.page.click("text=Elements")
        self.page.click("text=Web Tables")
        
    def click_add_button(self):
        self.page.locator(self.add_button).click()
        
    def is_modal_visible(self) -> bool:
        return self.page.locator(self.modal_form).is_visible()
        
    def enter_first_name(self, name: str):
        self.page.locator(self.first_name_input).fill(name)
        
    def enter_last_name(self, name: str):
        self.page.locator(self.last_name_input).fill(name)
        
    def enter_email(self, email: str):
        self.page.locator(self.email_input).fill(email)
        
    def enter_age(self, age: str):
        self.page.locator(self.age_input).fill(age)
        
    def enter_salary(self, salary: str):
        self.page.locator(self.salary_input).fill(salary)
        
    def enter_department(self, department: str):
        self.page.locator(self.department_input).fill(department)
        
    def click_submit(self):
        self.page.locator(self.submit_button).click()
        
    def add_record(self, first_name: str, last_name: str, email: str, age: str, salary: str, department: str):
        self.click_add_button()
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_age(age)
        self.enter_salary(salary)
        self.enter_department(department)
        self.click_submit()

