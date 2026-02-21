import pytest
import allure
import random
from pytest_check import check
from faker import Faker

faker = Faker()


@allure.epic("Cinescope")
@allure.feature("Allure Examples")
@allure.suite("Демонстрационные примеры")
class TestAllureExamples:

    @allure.story("Soft Asserts")
    @allure.title("Пример использования Soft Asserts для проверки данных пользователя")
    @allure.description("""
    Этот тест демонстрирует использование soft asserts (pytest-check).
    Soft asserts позволяют продолжить выполнение теста даже после провала одной проверки.
    Все ошибки собираются и отображаются в конце теста.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_soft_asserts_user_validation(self):

        with allure.step("Подготовка тестовых данных пользователя"):
            # Симулируем ответ от API
            mock_user_response = {
                "id": "12345",
                "email": "test@example.com",
                "fullName": "Test User",
                "verified": True,
                "banned": False,
                "roles": ["USER"]
            }
            allure.attach(str(mock_user_response), name="Mock User Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Ожидаемые данные пользователя"):
            expected_data = {
                "id": "12345",
                "email": "test@example.com",
                "fullName": "INCORRECT_NAME",  # Намеренная ошибка для демонстрации
                "verified": True,
                "banned": False,
                "roles": ["USER"]
            }
            allure.attach(str(expected_data), name="Expected Data", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Проверка полей пользователя с использованием soft asserts"):
            with check:
                check.equal(mock_user_response["id"], expected_data["id"], "Проверка ID пользователя")
                check.equal(mock_user_response["email"], expected_data["email"], "Проверка Email")
                # Эта проверка провалится, но тест продолжит выполнение
                check.equal(mock_user_response["fullName"], expected_data["fullName"], "Проверка FullName")
                check.equal(mock_user_response["verified"], expected_data["verified"], "Проверка Verified")
                check.equal(mock_user_response["banned"], expected_data["banned"], "Проверка Banned")
                check.equal(mock_user_response["roles"], expected_data["roles"], "Проверка Roles")

    @allure.story("Soft Asserts")
    @allure.title("Пример использования Soft Asserts для валидации фильма")
    @allure.description("Проверка нескольких полей фильма с использованием soft asserts")
    @allure.severity(allure.severity_level.NORMAL)
    def test_soft_asserts_movie_validation(self):

        with allure.step("Создание тестовых данных фильма"):
            movie_response = {
                "id": 1,
                "name": "Test Movie",
                "price": 500,
                "description": "Test Description",
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
            allure.attach(str(movie_response), name="Movie Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Проверка обязательных полей фильма"):
            with check:
                check.is_not_none(movie_response.get("id"), "ID фильма не должен быть None")
                check.is_not_none(movie_response.get("name"), "Название фильма не должно быть None")
                check.greater(movie_response.get("price", 0), 0, "Цена должна быть больше 0")
        
        with allure.step("Проверка диапазонов значений"):
            with check:
                check.greater_equal(movie_response.get("price", 0), 100, "Цена должна быть >= 100")
                check.less_equal(movie_response.get("price", 0), 1000, "Цена должна быть <= 1000")
                check.is_in(movie_response.get("location"), ["MSK", "SPB"], "Локация должна быть MSK или SPB")

    @allure.story("Retries")
    @allure.title("Пример теста с автоматическими перезапусками (flaky test)")
    @allure.description("""
    Этот тест демонстрирует использование pytest-rerunfailures для автоматического 
    перезапуска упавших тестов. Полезно для тестов, которые могут падать из-за 
    временных проблем (сеть, нагрузка и т.д.)
    """)
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_with_retries_flaky(self):

        with allure.step("Генерация случайного результата"):
            result = random.choice([True, True, True, False])  # 75% шанс успеха
            allure.attach(f"Result: {result}", name="Random Result", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Проверка результата"):
            assert result, "Тест упал, но будет автоматически перезапущен"

    @allure.story("Вложенные шаги")
    @allure.title("Пример теста с вложенными шагами Allure")
    @allure.description("Демонстрация использования вложенных шагов для структурирования теста")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_nested_steps(self):

        with allure.step("Шаг 1: Подготовка данных"):
            with allure.step("Шаг 1.1: Генерация данных пользователя"):
                user_data = {
                    "email": faker.email(),
                    "fullName": faker.name()
                }
                allure.attach(str(user_data), name="User Data", attachment_type=allure.attachment_type.JSON)
            
            with allure.step("Шаг 1.2: Генерация данных фильма"):
                movie_data = {
                    "name": faker.catch_phrase(),
                    "price": faker.random_int(min=100, max=500)
                }
                allure.attach(str(movie_data), name="Movie Data", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Шаг 2: Валидация данных"):
            with allure.step("Шаг 2.1: Проверка email"):
                assert "@" in user_data["email"], "Email должен содержать @"
            
            with allure.step("Шаг 2.2: Проверка цены"):
                assert 100 <= movie_data["price"] <= 500, "Цена должна быть в диапазоне 100-500"

    @allure.story("Комбинированный пример")
    @allure.title("Комплексный тест с Soft Asserts, вложенными шагами и attachments")
    @allure.description("""
    Комплексный пример, объединяющий:
    - Soft asserts для множественных проверок
    - Вложенные шаги для структуризации
    - Различные типы attachments (JSON, TEXT)
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("demo", "complex")
    def test_complex_example(self):

        with allure.step("Этап 1: Подготовка тестовых данных"):
            with allure.step("Создание данных для регистрации"):
                registration_data = {
                    "email": faker.email(),
                    "password": faker.password(),
                    "fullName": faker.name()
                }
                allure.attach(str(registration_data), name="Registration Data", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Этап 2: Симуляция ответа от сервера"):
            server_response = {
                "id": faker.uuid4(),
                "email": registration_data["email"],
                "fullName": registration_data["fullName"],
                "verified": True,
                "createdAt": faker.iso8601()
            }
            allure.attach(str(server_response), name="Server Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Этап 3: Валидация ответа сервера"):
            with allure.step("Проверка обязательных полей"):
                with check:
                    check.is_not_none(server_response.get("id"), "ID не должен быть None")
                    check.is_not_none(server_response.get("email"), "Email не должен быть None")
                    check.is_not_none(server_response.get("createdAt"), "CreatedAt не должен быть None")
            
            with allure.step("Проверка соответствия данных"):
                with check:
                    check.equal(server_response["email"], registration_data["email"], "Email должен совпадать")
                    check.equal(server_response["fullName"], registration_data["fullName"], "FullName должен совпадать")
                    check.is_true(server_response["verified"], "Пользователь должен быть верифицирован")
