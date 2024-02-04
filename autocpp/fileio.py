from os import path
from abc import ABC


class CxxProjectIO(object):
    CMAKE_KEY = "CMake"

    def __init__(self, folder_path: str, cmake: bool) -> None:
        if folder_path is None or "":
            raise Exception("folder path is none or empty")
        if not path.exists(folder_path) or not path.isdir(folder_path):
            raise Exception("folder path not exists or is not a path to folder")
        self.folder_path: str = folder_path.replace("\\", "/")
        self.cmake: bool = cmake
        with open(self.folder_path, mode="r", encoding="utf-8") as f:
            self.content: str = f.readlines()
        self.line_count: int = len(self.content)

    # def config_cmake(self, configs: dict):
    #     if not self.cmake:
    #         return
    #     if self.CMAKE_KEY in configs.keys():
    #         configs = configs[self.CMAKE_KEY]
    
    
