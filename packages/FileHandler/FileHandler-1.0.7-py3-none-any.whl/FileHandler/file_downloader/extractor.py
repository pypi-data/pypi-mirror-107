from zipfile import ZipFile, BadZipFile
from pathlib import Path
from file_downloader.remover import FileRemover, DirCleaner


class ZipExtractor:

    @classmethod
    def extract_all(cls, filename, path="", stored_path="", stored_dir=""):
        storage_dest = Path(stored_path).joinpath(stored_dir)
        if storage_dest.exists() and storage_dest.is_dir():
            DirCleaner(storage_dest).remove_dir_files()
        replaced_filename = cls.__clean_file_extra_extensions(filename)
        extract_item_name = Path(path).joinpath(f"{replaced_filename}.zip")
        if not extract_item_name.exists() or not extract_item_name.is_file():
            raise Exception
        try:
            with ZipFile(extract_item_name, "r") as zipObj:
                zipObj.extractall(Path(stored_path).joinpath(stored_dir))
        except BadZipFile:
            return FileRemover(filename=extract_item_name)

        return FileRemover(filename=extract_item_name)

    @staticmethod
    def __clean_file_extra_extensions(source_filename):
        return source_filename.replace(".zip", "")
