import os
import json
from datetime import datetime
from utils.helpers import log, detect_and_read

# os.chdir('Dz_12/project_root') # при запуске из файла

log("=== Начало сериализации ===", log_name="serialize.log")

raw_dir = "data/raw"
processed_dir = "data/processed"
output_file = "output/processed_data.json"

os.makedirs("output", exist_ok=True)
result = []

for filename in sorted(os.listdir(processed_dir)):
    processed_path = os.path.join(processed_dir, filename)
    if not os.path.isfile(processed_path):
        continue

    # Получаем имя исходного файла (убираем _processed)
    name, ext = os.path.splitext(filename)
    if name.endswith("_processed"):
        original_name = name[:-10] + ext
    else:
        original_name = filename
    raw_path = os.path.join(raw_dir, original_name)

    processed_text = detect_and_read(processed_path)
    original_text = detect_and_read(raw_path) if os.path.exists(raw_path) else None

    stat = os.stat(processed_path)
    size_bytes = stat.st_size
    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "filename": filename,
        "original_text": original_text,
        "processed_text": processed_text,
        "size_bytes": size_bytes,
        "last_modified": mod_time,
    }
    result.append(entry)
    log(f"Обработан: {filename} | размер: {size_bytes} байт")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

log(f"JSON сохранён: {output_file} | записей: {len(result)}", log_name="serialize.log")
log("Сериализация завершена", log_name="serialize.log")
