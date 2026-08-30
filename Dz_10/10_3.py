class NegativeNumberError(Exception):
    """Исключение, которое генерируется при передаче отрицательного числа."""

    def __init__(self, number): 
        self.number = number
        self.message = "Число не должно быть отрицательным"  
        super().__init__(self.message)  # Вызываем конструктор базового класса Exception

    def __str__(self):
        return f"NegativeNumberError: {self.message} (число: {self.number})"

def check_positive_number(number):
    if number < 0:
        raise NegativeNumberError(number)  # Возбуждаем исключение с переданным числом
    return number  # Если число неотрицательное, возвращаем его

def check_number(number):
    try:
        check_positive_number(number)     
    except NegativeNumberError as e:
        print(e)  
    else:
        print(check_positive_number(number))

# Проверка работоспособности
check_number(10)
check_number(-5)

'''
10
NegativeNumberError: Число не должно быть отрицательным (число: -5)
'''