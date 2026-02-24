import pytest
import json
from pydantic import ValidationError
from Cinescope_exam.models.base_models import RegistrationUserModel, Product, ProductType


class TestPydanticValidation:
    """Тесты валидации Pydantic моделей"""

    def test_validate_test_user(self, test_user):

        print(f"\n Исходные данные test_user:\n{test_user}")
        test_user_dict = test_user.model_dump() if hasattr(test_user, 'model_dump') else test_user
        user = RegistrationUserModel(**test_user_dict)
        json_output = user.model_dump_json(exclude_unset=True, indent=2)
        print(f"\n test_user JSON (exclude_unset=True):\n{json_output}")

        assert user.email == test_user_dict['email']

    def test_validate_creation_user_data(self, creation_user_data):
        print(f"\n Исходные данные creation_user_data:\n{creation_user_data}")
        creation_user_dict = creation_user_data.model_dump() if hasattr(creation_user_data, 'model_dump') else creation_user_data
        user = RegistrationUserModel(**creation_user_dict)
        json_output = user.model_dump_json(indent=2)
        print(f"\n creation_user_data JSON (exclude_unset=False):\n{json_output}")

        assert user.verified == True
        assert user.banned == False

    def test_compare_outputs(self, test_user, creation_user_data):
        test_user_dict = test_user.model_dump() if hasattr(test_user, 'model_dump') else test_user
        creation_user_dict = creation_user_data.model_dump() if hasattr(creation_user_data, 'model_dump') else creation_user_data

        user1 = RegistrationUserModel(**test_user_dict)
        json1 = user1.model_dump_json(exclude_unset=True, indent=2)

        user2 = RegistrationUserModel(**creation_user_dict)
        json2 = user2.model_dump_json(indent=2)

        print(f"\n test_user (exclude_unset=True):\n{json1}")
        print(f"\n creation_user_data (exclude_unset=False):\n{json2}")

        print(" АНАЛИЗ:")
        print("exclude_unset=True  → Убирает None поля")
        print("exclude_unset=False → Показывает все поля")


class TestCustomValidators:
    """Тесты кастомных валидаторов"""

    def test_valid_email_and_password(self):
        """Успешная валидация - правильный email и пароль"""
        valid_data = {
            "email": "user@example.com",
            "fullName": "John Doe",
            "password": "SecurePass123",
            "passwordRepeat": "SecurePass123",
            "roles": ["USER"]
        }
        
        user = RegistrationUserModel(**valid_data)
        print(f"\nУспешная валидация:\n{user.model_dump_json(indent=2)}")
        
        assert user.email == "user@example.com"
        assert user.password == "SecurePass123"

    def test_invalid_email_without_at(self):
        """Ошибка валидации - email без '@'"""
        invalid_data = {
            "email": "userexample.com",
            "fullName": "John Doe",
            "password": "SecurePass123",
            "passwordRepeat": "SecurePass123",
            "roles": ["USER"]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            RegistrationUserModel(**invalid_data)
        
        print(f"\nОшибка валидации email:\n{exc_info.value}")
        assert "Email должен содержать '@'" in str(exc_info.value)

    def test_invalid_password_too_short(self):
        """Ошибка валидации - пароль меньше 8 символов"""
        invalid_data = {
            "email": "user@example.com",
            "fullName": "John Doe",
            "password": "short",
            "passwordRepeat": "short",
            "roles": ["USER"]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            RegistrationUserModel(**invalid_data)
        
        print(f"\nОшибка валидации пароля:\n{exc_info.value}")
        assert "Пароль должен содержать не меньше 8 символов" in str(exc_info.value)

    def test_multiple_validation_errors(self):
        """Ошибка валидации - несколько ошибок одновременно"""
        invalid_data = {
            "email": "bademail",
            "fullName": "John Doe",
            "password": "123",
            "passwordRepeat": "123",
            "roles": ["USER"]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            RegistrationUserModel(**invalid_data)
        
        error_str = str(exc_info.value)
        print(f"\nМножественные ошибки валидации:\n{exc_info.value}")
        
        assert "Email должен содержать '@'" in error_str
        assert "Пароль должен содержать не меньше 8 символов" in error_str


class TestProductSerialization:
    """Тесты сериализации и десериализации Product"""

    def test_product_serialization_deserialization(self):
        """Полный цикл: создание объекта -> JSON -> обратно в объект"""
        
        product = Product(
            name="Ноутбук MSI",
            price=999.99,
            in_stock=True,
            product_type=ProductType.ELECTRONICS
        )
        
        print(f"\n1. Исходный объект Product:\n{product}")

        json_data = product.model_dump_json(indent=2)
        print(f"\n2. Сериализованный JSON:\n{json_data}")
        product_dict = json.loads(json_data)
        restored_product = Product(**product_dict)
        
        print(f"\n3. Восстановленный объект:\n{restored_product}")

        assert restored_product.name == product.name
        assert restored_product.price == product.price
        assert restored_product.in_stock == product.in_stock
        assert restored_product.product_type == product.product_type

    def test_multiple_products_serialization(self):
        """Сериализация списка продуктов"""
        
        products = [
            Product(name="Телефон", price=599.99, in_stock=True, product_type=ProductType.ELECTRONICS),
            Product(name="Куртка", price=89.99, in_stock=False, product_type=ProductType.CLOTHING),
            Product(name="Хлеб", price=2.50, in_stock=True, product_type=ProductType.FOOD),
        ]
        
        products_json = json.dumps([p.model_dump() for p in products], indent=2, ensure_ascii=False)
        print(f"\nСписок продуктов в JSON:\n{products_json}")
        products_data = json.loads(products_json)
        restored_products = [Product(**p) for p in products_data]
        
        assert len(restored_products) == 3
        assert restored_products[0].product_type == ProductType.ELECTRONICS
        assert restored_products[1].product_type == ProductType.CLOTHING
        assert restored_products[2].in_stock == True

    def test_product_invalid_type(self):
        """Ошибка валидации при неправильном типе продукта"""
        
        invalid_data = {
            "name": "Товар",
            "price": 100.0,
            "in_stock": True,
            "product_type": "Неизвестный тип"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Product(**invalid_data)
        
        print(f"\nОшибка валидации типа продукта:\n{exc_info.value}")
        assert "product_type" in str(exc_info.value)

    def test_product_json_schema(self):
        """Генерация JSON Schema для модели Product"""
        
        schema = Product.model_json_schema()
        print(f"\nJSON Schema для Product:\n{json.dumps(schema, indent=2, ensure_ascii=False)}")

        assert "properties" in schema
        assert "name" in schema["properties"]
        assert "price" in schema["properties"]
        assert "in_stock" in schema["properties"]
        assert "product_type" in schema["properties"]
