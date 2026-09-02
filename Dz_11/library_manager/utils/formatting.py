#from library_manager.catalog import Library

def format_book_data(data: dict) -> str:
  # Форматирует данные книги для вывода в отчет.
  # Пример формата: Title: {title}, Author: {author}, Genre: {genre}.
    title = data.get('title', 'N/A') # если данных нет, возвращаем N/A
    author = data.get('author', 'N/A')
    genre = data.get('genre', 'N/A')

    return f"Название: {title}, Автор: {author}, Жанр: {genre}"