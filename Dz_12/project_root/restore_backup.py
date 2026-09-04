import os
import zipfile
from utils.helpers import log

# os.chdir('Dz_12/project_root') # при запуске из файла

backups_dir = "backups"
data_dir = "data"

archives = [f for f in os.listdir(backups_dir) if f.startswith("backup_") and f.endswith(".zip")]
if not archives:
    log("Архивы не найдены!", log_name="restore.log")
    raise FileNotFoundError("В директории backups/ нет архивов для восстановления.")

archives.sort()
latest_backup = archives[-1]
backup_path = os.path.join(backups_dir, latest_backup)
log(f"Выбран архив для восстановления: {latest_backup}", log_name="restore.log")

with zipfile.ZipFile(backup_path, "r") as zipf:
    # Создаём нужные папки
    for name in zipf.namelist():
        if not name.endswith("/"):
            os.makedirs(os.path.dirname(name), exist_ok=True)
    zipf.extractall(".")
    log("Файлы извлечены из архива", log_name="restore.log")

    archived_files = [n for n in zipf.namelist() if not n.endswith("/")]
    restored_files = []
    for root, _, files in os.walk(data_dir):
        for f in files:
            restored_files.append(os.path.relpath(os.path.join(root, f), "."))

    log(f"В архиве было файлов: {len(archived_files)}", log_name="restore.log")
    log(f"На диске восстановлено файлов: {len(restored_files)}", log_name="restore.log")

    if len(archived_files) == len(restored_files):
        log("Проверка целостности: количество файлов совпадает.", log_name="restore.log")
    else:
        log("Внимание: количество файлов не совпадает!", log_name="restore.log")

log("Восстановление завершено", log_name="restore.log")
