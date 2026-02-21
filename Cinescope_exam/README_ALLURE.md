# Allure в проекте Cinescope - Быстрый старт

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск тестов
```bash
# Запустить все тесты
pytest tests/

# Запустить примеры Allure
pytest tests/api/test_allure_examples.py

# Запустить тесты Movies API с Allure
pytest tests/api/test_movies_api.py

# Запустить тесты User с Allure
pytest tests/back/test_user.py
```

Отчеты автоматически сохраняются в папку `allure-results/`

### 3. Просмотр отчетов

#### Windows (через Scoop)
```powershell
# Установка Scoop (если не установлен)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Установка Allure
scoop install allure

# Просмотр отчета
allure serve allure-results
```

После выполнения команды `allure serve` откроется браузер с интерактивным отчетом.

## 📊 Что включено

### ✅ Конфигурация
- `pytest.ini` - настроен для автоматической генерации Allure отчетов
- `.gitignore` - добавлены папки `allure-results/` и `allure-report/`
- `requirements.txt` - все необходимые библиотеки

### ✅ Примеры тестов

**test_allure_examples.py** - демонстрационные примеры:
- 🔸 Soft asserts для валидации данных
- 🔸 Автоматические перезапуски (retries) для нестабильных тестов
- 🔸 Вложенные шаги
- 🔸 Attachments (JSON, TEXT)
- 🔸 Комплексные примеры

**test_movies_api.py** - реальные тесты с Allure:
- ✨ `test_get_movies` - получение списка фильмов
- ✨ `test_create_movie` - создание фильма
- ✨ `test_delete_movie_super_admin` - проверка прав доступа

**test_user.py** - тесты User API с Allure:
- ✨ `test_create_user` - создание пользователя
- ✨ `test_get_user_by_locator` - получение по ID и Email
- ✨ `test_create_movie_user_role_forbidden` - проверка ролей

## 📚 Основные возможности

### Allure декораторы

```python
import allure

@allure.epic("Cinescope")
@allure.feature("Movies API")
@allure.story("CRUD операции")
@allure.title("Создание фильма")
@allure.severity(allure.severity_level.CRITICAL)
def test_example():
    with allure.step("Шаг 1: Подготовка данных"):
        # код
        pass
    
    with allure.step("Шаг 2: Отправка запроса"):
        # код
        allure.attach(str(data), name="Request", attachment_type=allure.attachment_type.JSON)
```

### Soft Asserts

```python
from pytest_check import check

with check:
    check.equal(actual, expected, "Проверка значения")
    check.is_not_none(value, "Значение не должно быть None")
    # Продолжит выполнение даже если проверка провалилась
```

### Автоматические перезапуски

```python
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_flaky():
    # Тест будет перезапущен до 3 раз при падении
    pass
```

## 📖 Полная документация

Подробное руководство смотрите в файле [ALLURE_GUIDE.md](ALLURE_GUIDE.md)

## 🎯 Структура отчета Allure

После запуска `allure serve allure-results` вы увидите:

- **Overview** - общая статистика, графики, тренды
- **Behaviors** - группировка по Epic → Feature → Story
- **Suites** - группировка по тестовым наборам
- **Graphs** - визуализация распределения тестов
- **Timeline** - временная шкала выполнения

## 💡 Советы

1. **Очистка старых отчетов**: Папка `allure-results` автоматически очищается при каждом запуске pytest (настроено `--clean-alluredir`)

2. **Запуск конкретного теста**:
   ```bash
   pytest tests/api/test_movies_api.py::TestMovies::test_get_movies -v
   ```

3. **Просмотр отчета без установки Allure**:
   - Используйте Allure в Docker
   - Или интегрируйте с CI/CD (Jenkins, GitLab CI)

## 🔗 Полезные ссылки

- [Официальная документация Allure](https://allurereport.org/docs/)
- [pytest-check](https://github.com/okken/pytest-check)
- [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures)

---

**Готово! 🎉** Теперь у вас есть полноценная интеграция Allure в проекте Cinescope!
