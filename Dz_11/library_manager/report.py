from library_manager.catalog import Library

def generate_report(library: Library) -> str:
  # Генерирует отчет о всех книгах в библиотеке в формате строки.
    if not library.books:
        return "Отчёт: в библиотеке нет книг."

    lines = ["=== Отчёт по библиотеке ===", f"Всего книг: {len(library.books)}", ""]
    for idx, book in enumerate(library.books, start=1):
        lines.append(f"{idx}. \"{book['title']}\" — {book['author']} ({book['genre']})")
    lines.append("===========================")

    return "\n".join(lines)