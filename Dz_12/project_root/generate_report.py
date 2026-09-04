# generate_report.py
import os
import json
from datetime import datetime
from utils.helpers import log

os.makedirs("output", exist_ok=True)

# --- Данные о выполненных заданиях ---
tasks = [
    {
        "step": 1,
        "title": "Создание структуры директорий",
        "description": "Создание project_root/ с вложенными папками data/raw, data/processed, logs, backups, output.",
        "difficulties": "Ошибки при повторном запуске: os.mkdir() падает, если папка уже существует.",
        "solution": "Использовали os.makedirs(..., exist_ok=True) вместо os.mkdir().",
        "time_spent": "10 минут",
    },
    {
        "step": 2,
        "title": "Создание тестовых файлов с разными кодировками",
        "description": "Запись файлов в UTF-8 и ISO-8859-1 с текстами на разных языках.",
        "difficulties": "ISO-8859-1 не поддерживает кириллицу — запись русского текста вызывала UnicodeEncodeError.",
        "solution": "Для ISO-8859-1 использовали только испанский и немецкий тексты. Русский — только в UTF-8.",
        "time_spent": "15 минут",
    },
    {
        "step": 3,
        "title": "Чтение и обработка данных",
        "description": "Чтение файлов из data/raw/, замена регистра (swapcase), сохранение в data/processed/.",
        "difficulties": "Нужно было корректно определить кодировку каждого файла при чтении.",
        "solution": "Написали функцию detect_and_read() с перебором кодировок: UTF-8 → ISO-8859-1 → CP1251 → ASCII.",
        "time_spent": "20 минут",
    },
    {
        "step": 4,
        "title": "Сериализация в JSON",
        "description": "Сбор данных из data/processed/ в один JSON-файл с метаданными.",
        "difficulties": "Нужно было получить исходный текст до обработки, но в processed лежат уже изменённые файлы.",
        "solution": "По имени обработанного файла восстанавливаем имя оригинала (убираем суффикс _processed) и читаем из data/raw/.",
        "time_spent": "20 минут",
    },
    {
        "step": 5,
        "title": "Создание резервной копии",
        "description": "Архивация data/ в backups/backup_YYYYMMDD.zip.",
        "difficulties": "Нужно было сохранить структуру папок внутри архива, а не только имена файлов.",
        "solution": "Использовали os.path.relpath() для записи относительных путей в arcname.",
        "time_spent": "15 минут",
    },
    {
        "step": 6,
        "title": "Восстановление данных",
        "description": "Распаковка архива и проверка целостности.",
        "difficulties": "Нужно было выбрать последний архив, если их несколько.",
        "solution": "Сортировка списка архивов по имени (дата в формате YYYYMMDD сортируется лексикографически). Проверка количества файлов после распаковки.",
        "time_spent": "15 минут",
    },
    {
        "step": 7,
        "title": "Вынесение общих функций в модуль utils",
        "description": "Рефакторинг: log и detect_and_read вынесены в utils/helpers.py.",
        "difficulties": "Импорт из utils работал только при запуске из project_root. При запуске из другой директории — ModuleNotFoundError.",
        "solution": "Фиксированный запуск из project_root. Можно улучшить через sys.path.insert или setup.py.",
        "time_spent": "15 минут",
    },
]

conclusions = [
    "Проект успешно реализован: все скрипты работают с разными кодировками и логируют операции.",
    "Вынесение общих функций в модуль utils/helpers.py упростило повторное использование кода.",
    "Функция detect_and_read с перебором кодировок оказалась универсальным решением для чтения файлов.",
    "Логирование в отдельные файлы (process.log, serialize.log, backup.log, restore.log) помогает отслеживать ошибки.",
]

improvements = [
    "Добавить проверку целостности через хеши (MD5/SHA-256) при бэкапе и восстановлении.",
    "Реализовать автоудаление старых архивов (оставлять только N последних копий).",
    "Добавить обработку вложенных директорий в data/raw/ (рекурсивный обход).",
    "Интегрировать pytest для тестирования функций validate_book_data, format_book_data и detect_and_read.",
    "Добавить конфигурационный файл (config.yaml или .env) для путей и кодировок вместо жёстко заданных значений.",
    "Настроить pre-commit хуки для автоматической проверки перед коммитом.",
]

report = {
    "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "project": "Library Data Processing Project",
    "tasks": tasks,
    "conclusions": conclusions,
    "proposed_improvements": improvements,
}

# --- Сохранение в JSON ---
json_path = "output/final_report.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
log(f"JSON-отчёт сохранён: {json_path}", log_name="report.log")

# --- Сохранение в текстовом формате ---
txt_path = "output/final_report.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(f"ИТОГОВЫЙ ОТЧЁТ — {report['report_date']}\n")
    f.write(f"Проект: {report['project']}\n")
    f.write("=" * 60 + "\n\n")

    for t in tasks:
        f.write(f"Шаг {t['step']}. {t['title']}\n")
        f.write(f"  Описание: {t['description']}\n")
        f.write(f"  Трудности: {t['difficulties']}\n")
        f.write(f"  Решение: {t['solution']}\n")
        f.write(f"  Затрачено: {t['time_spent']}\n\n")

    f.write("ВЫВОДЫ\n")
    f.write("-" * 60 + "\n")
    for c in conclusions:
        f.write(f"• {c}\n")

    f.write("\nПРЕДЛАГАЕМЫЕ УЛУЧШЕНИЯ\n")
    f.write("-" * 60 + "\n")
    for i in improvements:
        f.write(f"• {i}\n")

log(f"Текстовый отчёт сохранён: {txt_path}", log_name="report.log")
log("Генерация отчёта завершена", log_name="report.log")
