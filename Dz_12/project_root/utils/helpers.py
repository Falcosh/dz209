import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

def log(msg: str, log_name: str = "app.log") -> None:
    """Записывает сообщение с временной меткой в лог-файл."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)  # вывод в консоль
    log_path = os.path.join(LOGS_DIR, log_name)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def detect_and_read(filepath: str) -> str:
    """
    Пытается прочитать файл, перебирая несколько кодировок.
    Возвращает содержимое как строку.
    """
    encodings = ["utf-8", "iso-8859-1", "cp1251", "ascii"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Не удалось прочитать файл с подходящей кодировкой: {filepath}")
