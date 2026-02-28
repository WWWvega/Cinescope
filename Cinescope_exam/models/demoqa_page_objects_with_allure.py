from playwright.sync_api import Page
import allure
from Cinescope_exam.models.page_actions import PageAction


class DemoQABasePage(PageAction):
    """Базовая логика доступная для всех страниц на сайте DemoQA"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "https://demoqa.com/"

    @allure.step("Переход на главную страницу DemoQA")
    def open(self):
        self.open_url(self.base_url)

    @allure.step("Переход в секцию: {section_name}")
    def navigate_to_section(self, section_name: str):
        self.click_element("text={0}".format(section_name))


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
        
    @allure.step("Открытие страницы Radio Button через навигацию")
    def open_via_navigation(self):
        self.open()
        self.navigate_to_section("Elements")
        self.click_element("text=Radio Button")
        
    @allure.step("Клик по радио-кнопке Yes")
    def click_yes_radio(self):
        self.click_element(self.yes_radio_label)
        
    @allure.step("Клик по радио-кнопке Impressive")
    def click_impressive_radio(self):
        self.click_element(self.impressive_radio_label)


class DemoQATextBoxPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}text-box"
        
        self.full_name_input = "input#userName"
        self.email_input = "input#userEmail"
        self.current_address_input = "textarea#currentAddress"
        self.permanent_address_input = "textarea#permanentAddress"
        self.submit_button = "button#submit"
        
    @allure.step("Открытие страницы Text Box через навигацию")
    def open_via_navigation(self):
        self.open()
        self.navigate_to_section("Elements")
        self.click_element("text=Text Box")
        
    @allure.step("Ввод имени: {name}")
    def enter_full_name(self, name: str):
        self.enter_text_to_element(self.full_name_input, name)
        
    @allure.step("Ввод email: {email}")
    def enter_email(self, email: str):
        self.enter_text_to_element(self.email_input, email)
        
    @allure.step("Ввод текущего адреса: {address}")
    def enter_current_address(self, address: str):
        self.enter_text_to_element(self.current_address_input, address)
        
    @allure.step("Ввод постоянного адреса: {address}")
    def enter_permanent_address(self, address: str):
        self.enter_text_to_element(self.permanent_address_input, address)
        
    @allure.step("Клик по кнопке Submit")
    def click_submit(self):
        self.click_element(self.submit_button)


class DemoQAPracticeFormPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}automation-practice-form"
        
        self.first_name_input = "#firstName"
        self.last_name_input = "#lastName"
        self.email_input = "#userEmail"
        self.gender_male_label = "label[for='gender-radio-1']"
        self.mobile_input = "#userNumber"
        self.subjects_input = "#subjectsInput"
        self.hobbies_sports = "label[for='hobbies-checkbox-1']"
        self.hobbies_reading = "label[for='hobbies-checkbox-2']"
        self.current_address_input = "#currentAddress"
        self.state_dropdown = "#state"
        self.city_dropdown = "#city"
        self.submit_button = "#submit"
        self.footer = "footer"
        self.modal_content = ".modal-content"
        
    @allure.step("Открытие страницы Practice Form через навигацию")
    def open_via_navigation(self):
        self.open()
        self.navigate_to_section("Forms")
        self.click_element("text=Practice Form")
        
    @allure.step("Заполнение формы")
    def fill_form(self, first_name: str, last_name: str, email: str, mobile: str, address: str):
        self.enter_text_to_element(self.first_name_input, first_name)
        self.page.locator(self.last_name_input).type(last_name)
        self.enter_text_to_element(self.email_input, email)
        self.click_element(self.gender_male_label)
        self.page.locator(self.mobile_input).type(mobile)
        self.enter_text_to_element(self.current_address_input, address)
        
    @allure.step("Добавление предмета: {subject}")
    def add_subject(self, subject: str):
        self.page.locator(self.subjects_input).type(subject)
        self.page.keyboard.press("Enter")
        
    @allure.step("Выбор хобби")
    def select_hobbies(self):
        self.click_element(self.hobbies_sports)
        self.click_element(self.hobbies_reading)
        
    @allure.step("Выбор штата и города")
    def select_state_and_city(self, state: str, city: str):
        self.click_element(self.state_dropdown)
        self.click_element(f"text={state}")
        self.click_element(self.city_dropdown)
        self.click_element(f"text={city}")
        
    @allure.step("Отправка формы")
    def submit_form(self):
        self.click_element(self.submit_button)


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
        
    @allure.step("Открытие страницы Web Tables через навигацию")
    def open_via_navigation(self):
        self.open()
        self.navigate_to_section("Elements")
        self.click_element("text=Web Tables")
        
    @allure.step("Клик по кнопке Add")
    def click_add_button(self):
        self.click_element(self.add_button)
        
    @allure.step("Ввод имени: {name}")
    def enter_first_name(self, name: str):
        self.enter_text_to_element(self.first_name_input, name)
        
    @allure.step("Ввод фамилии: {name}")
    def enter_last_name(self, name: str):
        self.enter_text_to_element(self.last_name_input, name)
        
    @allure.step("Ввод email: {email}")
    def enter_email(self, email: str):
        self.enter_text_to_element(self.email_input, email)
        
    @allure.step("Ввод возраста: {age}")
    def enter_age(self, age: str):
        self.enter_text_to_element(self.age_input, age)
        
    @allure.step("Ввод зарплаты: {salary}")
    def enter_salary(self, salary: str):
        self.enter_text_to_element(self.salary_input, salary)
        
    @allure.step("Ввод отдела: {department}")
    def enter_department(self, department: str):
        self.enter_text_to_element(self.department_input, department)
        
    @allure.step("Клик по кнопке Submit")
    def click_submit(self):
        self.click_element(self.submit_button)
        
    @allure.step("Добавление записи в таблицу")
    def add_record(self, first_name: str, last_name: str, email: str, age: str, salary: str, department: str):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_age(age)
        self.enter_salary(salary)
        self.enter_department(department)
        self.click_submit()


class DemoQACheckBoxPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}checkbox"
        
        self.home_element = "text=Home >> visible=true"
        self.toggle_button = ".rc-tree-switcher"
        self.desktop_element = "text=Desktop >> visible=true"
        
    @allure.step("Открытие страницы CheckBox")
    def open(self):
        self.open_url(self.url)
        
    @allure.step("Клик на кнопку toggle")
    def click_toggle_button(self):
        self.click_element(self.toggle_button)


class DemoQADynamicPropertiesPage(DemoQABasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}dynamic-properties"
        
        self.visible_after_element = "#visibleAfter"
        
    @allure.step("Открытие страницы Dynamic Properties")
    def open(self):
        self.open_url(self.url)
        
    @allure.step("Ожидание появления элемента visibleAfter")
    def wait_for_visible_after_element(self, timeout: int = 10000):
        self.wait_for_element(self.visible_after_element, state="visible")
