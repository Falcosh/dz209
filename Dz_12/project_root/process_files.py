import os
from utils.helpers import log, detect_and_read

# os.chdir('Dz_12/project_root')  # при запуске из файла

log("=== Начало обработки файлов ===", log_name="process.log")

raw_dir = "data/raw"
processed_dir = "data/processed"

for filename in sorted(os.listdir(raw_dir)):
    raw_path = os.path.join(raw_dir, filename)
    if not os.path.isfile(raw_path):
        continue

    # Читаем с автоопределением кодировки
    text = detect_and_read(raw_path)
    log(f"Прочитан: {filename}")

    # Меняем регистр
    processed_text = text.swapcase()

    # Сохраняем в data/processed/ с суффиксом _processed
    name, ext = os.path.splitext(filename)
    processed_name = f"{name}_processed{ext}"
    processed_path = os.path.join(processed_dir, processed_name)

    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(processed_text)
    log(f"Сохранён: {processed_name}")

log("Обработка завершена", log_name="process.log")