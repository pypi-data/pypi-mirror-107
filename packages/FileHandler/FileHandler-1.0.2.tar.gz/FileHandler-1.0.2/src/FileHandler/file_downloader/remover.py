import os
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class FileRemover:

    def __init__(self, filename, path=""):
        self.filename = filename
        self.path = path

    def remove_file(self):
        file = Path(self.path).joinpath(self.filename)
        if file.is_file():
            os.remove(file)
        else:
            logger.warning("指定對象並非檔案，無法進行刪除")


class DirCleaner:

    def __init__(self, path="", stored_dir=""):
        self.path = path
        self.stored_dir = stored_dir

    def remove_dir_files(self, delete_whole_directory=False):
        if not any((self.path, self.stored_dir)):
            logger.warning("欲刪除當前資料夾，無法執行該危險行為")
            return

        storage_dest = Path(self.path).joinpath(self.stored_dir)
        if delete_whole_directory:
            if storage_dest.exists() and storage_dest.is_dir():
                shutil.rmtree(storage_dest)
        else:
            for file in os.listdir(storage_dest):
                path = os.path.join(storage_dest, file)
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)
