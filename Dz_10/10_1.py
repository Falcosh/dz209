def convert_to_int(value):
    try:
        number = int(value)
    except ValueError:
        print(f"Ошибка: невозможно преобразовать строку '{value}' в число.")
    except BaseException as be:
        print("Ошибка: невозможно преобразовать строку в число.")
        print(f"Тип ошибки: {type(be).__name__}")
        print(f"Сообщение об ошибке: {be}")
    else:
        number = int(value)
        print(f"Строка '{value}' преобразована в число: {number}")
    finally:
        print('Преобразование завершено\n')

convert_to_int(123)
convert_to_int('123')
convert_to_int('abc')
convert_to_int([1, 2, 3])

'''
Строка 123 преобразована в число: 123
Преобразование завершено

Строка 123 преобразована в число: 123
Преобразование завершено

Ошибка: невозможно преобразовать строку abc в число.
Преобразование завершено

Ошибка: невозможно преобразовать строку в число.
Тип ошибки: TypeError
Сообщение об ошибке: int() argument must be a string, a bytes-like object or a real number, not 'list'
Преобразование завершено
'''