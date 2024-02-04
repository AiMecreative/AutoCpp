import os
import sys
import subprocess
import logging
from os import path
from logging import handlers
from .cxxproject import CxxProject


class Compiler(object):
    COMPILER_KEY = "Compiler"
    PATH_SYMBOL = "/"

    def __init__(self, configs: dict) -> None:
        if self.COMPILER_KEY in configs.keys():
            configs = configs[self.COMPILER_KEY]
        self.cmake_path: str = configs["cmake_path"]
        self.build_type: str = configs["build_type"]
        self.c_compiler_path: str = configs["c_path"]
        self.cxx_compiler_path: str = configs["cxx_path"]
        self.project_name: str = configs["project_name"]

        self.cmake_minimum_required: str = "cmake_minimum_required(VERSION {})\n".format(configs["cmake_min"])
        self.project: str = "project({})\n".format(configs["project_name"])
        self.set_cxx_standard: str = "set(CMAKE_CXX_STANDARD {})\n".format(configs["cxx_standard"])
        self.add_executable: str = "add_executable({})\n".format(configs["project_name"])

        self.main_file = ""
        self.cmake_lists_path = ""
        self.build_path = ""
        self.exe_path = ""
        self.log_path = ""
        self.logger = None

    def config_cmake(self, project_path: str, multifile: bool):
        """CMakeLists.txt construct, configure cmake"""
        cmake_content = [
            self.cmake_minimum_required,
            self.project,
            self.set_cxx_standard,
            self.add_executable,
        ]
        if multifile:
            files = [f for f in os.listdir(project_path) if len(f.split(".")) > 1]
            lib_files = ""
            print(files)
            for file in files:
                if not file.split(".")[1] in CxxProject.CXX_EXT:
                    continue
                if file.split(".")[0] == "main":
                    self.main_file = self.PATH_SYMBOL.join((project_path, file))
                else:
                    file = self.PATH_SYMBOL.join((project_path, file))
                    lib_files += file
                    lib_files += " "
            cmake_content.append("add_library(project_lib {})\n".format(lib_files))
            cmake_content.append("target_link_libraries({} PUBLIC project_lib)\n".format(self.project_name))
            self.cmake_lists_path = self.PATH_SYMBOL.join((project_path, "CMakeLists.txt"))
            self.build_path = self.PATH_SYMBOL.join((project_path, "build"))
            self.log_path = self.PATH_SYMBOL.join((project_path, "out.log"))
        else:
            self.main_file = project_path
            self.cmake_lists_path = self.PATH_SYMBOL.join((project_path.split("/")[0:-1], "CMakeLists.txt"))
            self.build_path = self.PATH_SYMBOL.join((project_path.split("/")[0:-1], "build"))
            self.log_path = self.PATH_SYMBOL.join((project_path.split("/")[0:-1], "out.log"))
        cmake_content.append("target_sources({} PUBLIC {})\n".format(self.project_name, self.main_file))
        with open(self.cmake_lists_path, "w", encoding="utf-8") as cmake:
            cmake.writelines(cmake_content)
        if not path.exists(self.build_path):
            os.makedirs(self.build_path)
        logger: logging.Logger = logging.getLogger(self.log_path)
        log_file_handler = logging.FileHandler(self.log_path)
        log_file_handler.setFormatter("%(levelname)s: %(message)s")
        logger.addHandler(log_file_handler)
        self.logger = logger
        try:
            cmake_config_cmd = [
                self.cmake_path,
                "-D CMAKE_BUILD_TYPE:STRING={}".format(self.build_type),
                "-D CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE",
                "-D CMAKE_C_COMPILER:FILEPATH={}".format(self.c_compiler_path),
                "-D CMAKE_CXX_COMPILER:FILEPATH={}".format(self.cxx_compiler_path),
                "-S {}".format(project_path if multifile else project_path.split("/")[0:-1]),
                "-B {}".format(self.build_path),
                "-G Ninja"
            ]
            self.logger.info(cmake_config_cmd)
            subprocess.call(cmake_config_cmd)
        except OSError:
            self.logger.error("cmake config error")

    def compile_project(self, project: CxxProject):
        try:
            os.chdir(self.build_path)
            cmake_compile_cmd = [
                "ninja"
            ]
            self.logger.info(cmake_compile_cmd)
            subprocess.call(cmake_compile_cmd)
            self.exe_path = self.PATH_SYMBOL.join((self.build_path, "{}.exe".format(self.project_name)))
        except OSError:
            self.logger.error("cmake compile error")

    def run_project(self, project: CxxProject):
        try:
            print(">>>> start running <<<<")
            os.chdir(self.build_path)
            cmake_run_cmd = [
                "{}".format(self.exe_path)
            ]
            self.logger.info(cmake_run_cmd)
            subprocess.call(cmake_run_cmd)
        except OSError:
            self.logger.error("cmake run error")
