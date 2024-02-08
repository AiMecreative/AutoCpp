import os
from typing import List, Dict
from .datamap import *


class CMakeTools(object):
    CMAKE_KEY = "CMake"
    CMAKE_CMD = ["config", "build", "run"]

    def __init__(self) -> None:
        self.templates: Dict = {
            "cmake_minimum_required": "cmake_minimum_required(VERSION {})\n",
            "project": "project({})\n",
            "set_cxx_standard": "set(CMAKE_CXX_STANDARD {})\n",
            "add_executable": "add_executable({})\n",
            "add_library": "add_library({} {})\n",
            "target_link_libraries": "target_link_libraries({} PUBLIC {})\n",
            "target_sources": "target_sources({} PUBLIC {})\n"
        }

        self.cli_options: Dict = {
            "build_type": "{} ",
            "export_cmd": "{} ",
            "c_compiler": "{} ",
            "cxx_compiler": "{} ",
            "build_path": "{} ",
            "project_path": "{} ",
            "generator": "{} "
        }

        self.cmake_contents: List = list()
        self.cmake_cli: Dict = dict()

    def add_template(self, key: str, sentence: str, update: bool = False):
        if key in self.templates.keys() and not update:
            raise Exception("key has been used, config `update=True` if you want modify it")
        self.templates[key] = sentence

    def cmake_lists(self, cmake_lists_path: str):
        if os.path.isdir(cmake_lists_path):
            cmake_lists_path += "/CMakeLists.txt" if cmake_lists_path[-1] != "/" else "CMakeLists.txt"
        with open(cmake_lists_path, "w") as cmake:
            cmake.writelines(self.cmake_contents)

    def set_cli(self, key: str, cmd: str, update: bool = False):
        if not key in self.CMAKE_CMD:
            return
        if key in self.cmake_cli and not update:
            raise Exception("key has been used, config `update=True` if you want modify it")
        self.cmake_cli[key] = cmd

    def show_templates(self):
        print(self.templates)

    def show_cli_options(self):
        print(self.cli_options)

    def cmake_init_mul(self, main_file: str, lib_files: str, cmake_configs: CMakeConfig) -> List[str]:
        """init cmake_lists contents and cmake command lines for multi-file projects"""
        t = self.templates
        return [
            t["cmake_minimum_required"].format(cmake_configs.CMakeMinVersion),
            t["project"].format(cmake_configs.ProjectName),
            t["set_cxx_standard"].format(cmake_configs.CXXStandard),
            t["add_executable"].format(cmake_configs.ProjectName),
            t["add_library"].format(cmake_configs.LibName, lib_files),
            t["target_link_libraries"].format(cmake_configs.ProjectName, cmake_configs.LibName),
            t["target_sources"].format(cmake_configs.ProjectName, main_file)
        ]

    def cmake_init_slg(self, main_file: str, cmake_configs: CMakeConfig) -> List[str]:
        """init cmake_lists contents and cmake command lines for single file project"""
        t = self.templates
        return [
            t["cmake_minimum_required"].format(cmake_configs.CMakeMinVersion),
            t["project"].format(cmake_configs.ProjectName),
            t["set_cxx_standard"].format(cmake_configs.CXXStandard),
            t["add_executable"].format(cmake_configs.ProjectName),
            t["target_sources"].format(cmake_configs.ProjectName, main_file)
        ]
