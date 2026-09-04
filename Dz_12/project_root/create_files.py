import os
from utils.helpers import log

# переходим в корневую папку
# os.chdir('Dz_12/project_root') # при запуске из файла

# Файлы с разными языками и кодировками
files = [
    {'name': 'en_utf8.txt', 'content': 'Book: The Great Gatsby, Author: F. Scott Fitzgerald, Genre: Fiction', 'encoding': 'utf-8'},
    {'name': 'ru_utf8.txt', 'content': 'Книга: Мастер и Маргарита, Автор: М. Булгаков, Жанр: Мистика', 'encoding': 'utf-8'},
    {'name': 'es_iso88591.txt', 'content': 'Libro: Cien años de soledad, Autor: Gabriel García Márquez, Género: Realismo mágico', 'encoding': 'iso-8859-1'},
    {'name': 'de_iso88591.txt', 'content': 'Buch: Faust, Autor: Johann Wolfgang von Goethe, Genre: Drama', 'encoding': 'iso-8859-1'},
]

for f in files:
    path = os.path.join('data/raw', f['name'])
    with open(path, 'w', encoding=f['encoding']) as out:
        out.write(f['content'])
    log(f"Создан файл: {path} (кодировка: {f['encoding']})")

log('Инициализация завершена')