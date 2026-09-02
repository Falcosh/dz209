from .utils.data_validation import validate_book_data
from .utils.formatting import format_book_data

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, genre):
        # Добавление книги (с атрибутами: название, автор, жанр).
        book = {'title': title, 'author': author, 'genre': genre}
        if validate_book_data(book):
            self.books.append(book)
            print(f"Книга '{title}' добавлена в каталог.")
        else:
            print("Книга не добавлена в каталог - проверьте все ли поля заполнены.")


    def delete_book(title):
        # Удаление книги по названию.
        for i, book in enumerate(self.books):
            if book['title'] == title:
                removed_book = self.books.pop(i)
                print(f"Книга '{removed_book['title']}' удалена из каталога.")
                return
        print(f"Книга с названием '{title}' не найдена в каталоге.")

    # Поиск книги по названию, автору и жанру.
    def search_book(self, **kwargs):
        # Получаем параметры поиска с значениями по умолчанию None
        title = kwargs.get('title')
        author = kwargs.get('author')
        genre = kwargs.get('genre')

    # Если все параметры None, возвращаем пустой список
        if not title and not author and not genre:
            return []

        results = []

    # Проходим по всем книгам в коллекции
        for book in self.books:
            # Проверяем, подходит ли книга под заданные критерии
            # Используем .lower() для регистронезависимого поиска
            if (title is None or title.lower() in book['title'].lower()) and \
              (author is None or author.lower() in book['author'].lower()) and \
              (genre is None or genre.lower() in book['genre'].lower()):
                results.append(book)

        return results

    def all_books(self):
      # Просмотр всех книг в библиотеке.
        if not self.books:
            print("В библиотеке пока нет книг.")
            return

        print("\n--- Каталог книг ---\n")
        for book in self.books:
            print(format_book_data(book))#f"{book['title']} | {book['author']} | {book['genre']}")
        print("\n--------------------\n")