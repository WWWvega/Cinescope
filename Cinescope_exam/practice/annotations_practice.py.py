from typing import List
from typing import Optional
from typing import Union


def multiply(a: int, b: int) -> int:
    return a * b

print(multiply(5, 3))
print(multiply(10, -2))

# Это вызовет предупреждение IDE:
# print(multiply("5", "3"))

def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

print(sum_numbers([1, 2, 3, 4, 5]))
print(sum_numbers([10, 20, 30]))
print(sum_numbers([]))

# Это вызовет предупреждение IDE:
#print(sum_numbers(["one", "two", "three"]))
#print(sum_numbers("123"))

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

result1 = find_user(1)
result2 = find_user(2)
result3 = find_user(999)

print(result1)
print(result2)
print(result3)


def process_input(value: Union[int, str]) -> str:
    return f"Ты передал: {value}"

print(process_input(42))
print(process_input("привет"))
print(process_input(0))
print(process_input("123"))


class User:

    def __init__(self, name: str, age: int) -> None:
       self.name: str = name
       self.age: int = age

    def greet(self) -> str:
       return f"Привет, меня зовут {self.name}!"

user1 = User("Артем", 25)
print(user1.greet())  # "Привет, меня зовут Артем!"
print(f"Возраст: {user1.age}")  # "Возраст: 25"

user2 = User("Мария", 30)
print(user2.greet())  # "Привет, меня зовут Мария!"


def get_even_numbers(numbers: List[int]) -> List[int]:
    return [num for num in numbers if num % 2 == 0]


print(get_even_numbers([1, 2, 3, 4, 5, 6]))  # [2, 4, 6]
print(get_even_numbers([10, 15, 20, 25, 30]))  # [10, 20, 30]
print(get_even_numbers([1, 3, 5, 7, 9]))  # []
print(get_even_numbers([]))  # []