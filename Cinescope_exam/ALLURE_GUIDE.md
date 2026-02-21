# Руководство по использованию Allure в проекте Cinescope

## Установка

Все необходимые зависимости уже добавлены в `requirements.txt`:

```bash
pip install -r requirements.txt
```

Основные библиотеки:
- `allure-pytest` - интеграция Allure с pytest
- `pytest-check` - для soft asserts
- `pytest-rerunfailures` - для автоматических перезапусков тестов

## Запуск тестов с генерацией Allure отчетов

### Простой запуск
```bash
pytest tests/
```

Allure отчеты автоматически генерируются в папку `allure-results/` (настроено в `pytest.ini`)

### Запуск конкретных тестов
```bash
# Только примеры Allure
pytest tests/api/test_allure_examples.py

# Только тесты Movies API
pytest tests/api/test_movies_api.py

# Только тесты User
pytest tests/back/test_user.py
```

### Запуск с дополнительными параметрами
```bash
# Подробный вывод
pytest tests/ -v

# Показать print statements
pytest tests/ -s

# Запустить только тесты с определенным маркером
pytest tests/ -m "smoke"
```

## Просмотр Allure отчетов

### Установка Allure Commandline (Windows)

1. Установите Scoop (если еще не установлен):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

2. Установите Java (если не установлена):
   - Скачайте с https://www.oracle.com/java/technologies/downloads/
   - Или через Scoop: `scoop install openjdk`

3. Установите Allure:
```powershell
scoop install allure
```

### Генерация и просмотр отчета

```bash
# Генерация и автоматическое открытие в браузере
allure serve allure-results

# Или если allure не в PATH
C:\Users\<Имя_Пользователя>\scoop\apps\allure\current\bin\allure.bat serve allure-results
```

## Примеры использования Allure декораторов

### Базовая структура теста с Allure

```python
import allure
import pytest

@allure.epic("Название проекта")
@allure.feature("Функциональность")
@allure.suite("Набор тестов")
class TestExample:
    
    @allure.story("Конкретная история/фича")
    @allure.title("Название теста")
    @allure.description("Подробное описание что делает тест")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_example(self):
        with allure.step("Шаг 1: Описание действия"):
            # Код
            pass
        
        with allure.step("Шаг 2: Проверка результата"):
            # Assertions
            assert True
```

### Уровни важности (Severity)

```python
@allure.severity(allure.severity_level.BLOCKER)    # Блокер
@allure.severity(allure.severity_level.CRITICAL)   # Критический
@allure.severity(allure.severity_level.NORMAL)     # Обычный
@allure.severity(allure.severity_level.MINOR)      # Минорный
@allure.severity(allure.severity_level.TRIVIAL)    # Тривиальный
```

### Добавление вложений (Attachments)

```python
# Текст
allure.attach("Текстовые данные", name="log.txt", attachment_type=allure.attachment_type.TEXT)

# JSON
allure.attach(str(data), name="Response", attachment_type=allure.attachment_type.JSON)

# HTML
allure.attach("<h1>HTML</h1>", name="page", attachment_type=allure.attachment_type.HTML)

# Файл
allure.attach.file("path/to/file.png", name="Screenshot", attachment_type=allure.attachment_type.PNG)
```

### Динамические заголовки и описания

```python
@pytest.mark.parametrize("value", [1, 2, 3])
def test_dynamic(value):
    allure.dynamic.title(f"Тест со значением {value}")
    allure.dynamic.description(f"Проверка для значения: {value}")
```

## Soft Asserts (pytest-check)

Soft asserts позволяют продолжить выполнение теста даже после провала проверки:

```python
from pytest_check import check

def test_with_soft_asserts():
    with allure.step("Проверка нескольких условий"):
        with check:
            check.equal(1 + 1, 2, "Проверка сложения")
            check.equal(2 * 2, 4, "Проверка умножения")
            check.equal(3 - 1, 2, "Проверка вычитания")
            # Даже если одна проверка провалится, остальные выполнятся
```

### Встроенные функции pytest-check

```python
check.equal(a, b, msg)              # a == b
check.not_equal(a, b, msg)          # a != b
check.is_true(x, msg)               # x == True
check.is_false(x, msg)              # x == False
check.is_none(x, msg)               # x == None
check.is_not_none(x, msg)           # x != None
check.is_in(a, b, msg)              # a in b
check.is_not_in(a, b, msg)          # a not in b
check.greater(a, b, msg)            # a > b
check.less(a, b, msg)               # a < b
check.greater_equal(a, b, msg)      # a >= b
check.less_equal(a, b, msg)         # a <= b
```

## Автоматические перезапуски (Retries)

Для тестов, которые могут падать из-за временных проблем:

```python
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_flaky():
    # Тест будет перезапущен до 3 раз с задержкой в 1 секунду
    assert some_unstable_operation()
```

## Структура отчета Allure

После генерации отчета вы увидите:

### Overview
- Общая статистика выполнения тестов
- Графики и диаграммы
- Тренды выполнения

### Behaviors (Features by stories)
- Группировка по Epic → Feature → Story
- Иерархическая структура тестов

### Suites
- Группировка по тестовым наборам
- По файлам и классам

### Graphs
- Распределение тестов по статусам
- Распределение по важности (severity)
- Продолжительность выполнения

### Timeline
- Временная шкала выполнения тестов
- Параллельное выполнение

## Примеры в проекте

### 1. test_allure_examples.py
Демонстрационные примеры:
- Soft asserts для валидации данных
- Тесты с автоматическими перезапусками
- Вложенные шаги
- Комплексные примеры с attachments

### 2. test_movies_api.py
Реальные тесты Movies API с Allure:
- `test_get_movies` - получение списка фильмов
- `test_create_movie` - создание фильма
- `test_delete_movie_super_admin` - проверка прав доступа

### 3. test_user.py
Реальные тесты User API с Allure:
- `test_create_user` - создание пользователя
- `test_get_user_by_locator` - получение по ID и Email
- `test_create_movie_user_role_forbidden` - проверка ограничений ролей

## Рекомендации

1. **Используйте описательные названия шагов**
   ```python
   with allure.step("Отправка POST запроса на /movies"):
       # вместо просто "Отправка запроса"
   ```

2. **Добавляйте attachments для важных данных**
   ```python
   allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
   ```

3. **Группируйте тесты логически**
   ```python
   @allure.epic("Cinescope")
   @allure.feature("Movies API")
   @allure.story("CRUD операции")
   ```

4. **Используйте правильные severity levels**
   - CRITICAL для основного функционала
   - NORMAL для второстепенных проверок
   - MINOR/TRIVIAL для вспомогательных тестов

5. **Soft asserts для множественных проверок**
   - Используйте когда нужно проверить несколько полей
   - Помогает получить полную картину проблемы

## Полезные ссылки

- [Официальная документация Allure](https://allurereport.org/docs/)
- [Allure pytest reference](https://allurereport.org/docs/pytest-reference/)
- [pytest-check документация](https://github.com/okken/pytest-check)
- [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures)

## Troubleshooting

### Allure отчеты не генерируются
- Проверьте, что `allure-pytest` установлен
- Убедитесь, что в `pytest.ini` есть: `addopts = --alluredir=allure-results`

### Ошибка при просмотре отчета
- Убедитесь, что Java установлена: `java -version`
- Проверьте установку Allure: `allure --version`

### Тесты не запускаются
- Установите все зависимости: `pip install -r requirements.txt`
- Проверьте PYTHONPATH
