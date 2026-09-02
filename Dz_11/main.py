from library_manager.catalog import Library
from library_manager.report import generate_report
#from library_manager.utils.data_validation import validate_book_data
#from library_manager.utils.formatting import format_book_data

# проверка работоспособности

# Создаём библиотеку
my_library = Library()

# Добавляем книги
my_library.add_book("1984", "Джордж Оруэлл", "Фантастика")
my_library.add_book("Гарри Поттер", "Дж. К. Роулинг", "Фэнтези")
my_library.add_book("Букварь", "No author", "Учебная")
my_library.add_book("Приключения Шерлока Холмса", "А.Конан Дойль", "Детектив")
my_library.add_book("Властелин Колец", "Дж.Р.Толкин", "Фэнтези")
my_library.add_book("Корпорация Бессмертие", "Р.Шекли", "Фантастика")

# Выводим все книги (форматируем каждую строку)
my_library.all_books()

# функция поиска, выводит словарь
print('\n',my_library.search_book(title='Букварь'),'\n')

# Отчет о количестве книг
print(generate_report(my_library))

'''

generate_report()
'''