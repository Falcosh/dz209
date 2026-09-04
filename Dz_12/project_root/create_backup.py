import os
import zipfile
from datetime import datetime
from utils.helpers import log

#os.chdir('Dz_12/project_root') использовать при запуске файла. На терминале сменить дилекторию

log("Начало создания архива", log_name="backup.log")

data_dir = "data"
backups_dir = "backups"
os.makedirs(backups_dir, exist_ok=True)

date_str = datetime.now().strftime("%Y%m%d")
backup_filename = f"backup_{date_str}.zip"
backup_path = os.path.join(backups_dir, backup_filename)

with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, start=".")
            zipf.write(file_path, arcname=arcname)
            log(f"Добавлен в архив: {arcname}", log_name="backup.log")

log(f"Архив создан: {backup_path}", log_name="backup.log")