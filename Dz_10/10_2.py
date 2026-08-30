def validate_user(data):
    try:
        validate_user_input(data)
    except KeyError as e:
        print(f"Ошибка валидации: {e}")
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    except TypeError as e:
        print(f"Ошибка валидации: {e}")
    else:
        print("Данные корректные")


def validate_user_input(data):

    if not isinstance(data, dict):
        raise TypeError("Данные должны быть словарём")
    
    if 'name' not in data or 'age' not in data:
        if 'name' not in data:
            raise KeyError("В данных отсутствует ключ 'name'")
        if 'age' not in data:
            raise KeyError("В данных отсутствует ключ 'age'")
  
    name = data['name']
    if not isinstance(name, str):
        raise ValueError("Имя должно быть задано строкой")
    
    age = data['age']
    if not isinstance(age, (int, float)) or age < 0:
        raise ValueError("Возраст должен быть положительным числом")
    
    return True



# проверка работоспособности

user1 = {"name": "Alice", "age": 30}
user2 = {"age": 30}
user3 = {"name": "Alice", "age": -30}
user4 = "name: Alice"

validate_user(user1)
validate_user(user2)
validate_user(user3)
validate_user(user4)

'''
Данные корректные
Ошибка валидации: "В данных отсутствует ключ 'name'"
Ошибка валидации: Возраст должен быть положительным числом
Ошибка валидации: Данные должны быть словарём
'''