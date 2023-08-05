import requests
import os
from pathlib import Path


class Downloader:

    def __init__(self, url, filename, path=""):
        self.url = url
        self.path_filename = Path(path).joinpath(filename)
        self.response = None
        self.content = None

    def __send_request(self):
        self.response = requests.get(self.url)

    def __parse_response(self):
        self.content = self.response.content

    def __check_exists(self):
        if self.path_filename.exists() and self.path_filename.is_file():
            return True
        return False

    def __write_to_path(self):
        with open(self.path_filename, "wb") as code:
            code.write(self.content)

    def execute(self):
        self.__send_request()
        self.__parse_response()
        if self.__check_exists():
            os.remove(self.path_filename)
        self.__write_to_path()
