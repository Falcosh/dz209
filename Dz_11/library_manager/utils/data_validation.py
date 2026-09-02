#from library_manager.catalog import Library

def validate_book_data(data: dict) -> bool:
  # Проверяет корректность данных книги.
  #Например, проверяет, что все обязательные поля присутствуют и корректны.
    required_keys = {'title', 'author', 'genre'}
    return all(key in data for key in required_keys)