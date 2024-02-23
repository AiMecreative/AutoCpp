import re
from autocpp import Compiler
from pathlib import Path
from typing import List

class CProject(object):

    def __init__(self, project_path: Path, multifile: bool,
                 project_name: str = "task", lib_name: str = "tasklib",
                 mainfile_pattern: str=r"int main") -> None:
        self.project_path: Path = project_path
        self.mainfile_pattern: str = mainfile_pattern
        self.mainfile: Path = None
        self.libfiles: List[Path] = []
        self.multifile: bool = multifile
        self.project_name: str = project_name
        self.lib_name: str = lib_name
        self.score: float = 0.

        self.config_mainfile()
        self.config_libfiles()

    @property
    def is_multifile(self):
        return self.multifile
    
    def set_mainfile(self, mainfile: Path):
        self.mainfile = mainfile
    
    def config_mainfile(self):
        if not self.multifile: 
            self.mainfile = self.project_path
        project = self.project_path
        cpps = project.glob("*.cpp")
        for cpp in cpps:
            with cpp.open(mode="r", encoding="utf-8") as cpp_file:
                contents = str().join(cpp_file.readlines())
            results = re.search(pattern=self.mainfile_pattern, string=contents)
            if results is not None:
                self.mainfile: Path = project / cpp
        if self.mainfile is None:
            raise Exception("in {} no main cpp file was found".format((project.name)))
    
    def config_libfiles(self):
        project = self.project_path
        cpps = project.glob("*.cpp")
        hs = project.glob("*.h")
        hpps = project.glob("*.hpp")
        hs = [project / h for h in hs]
        hpps = [project / hpp for hpp in hpps]
        for cpp in cpps:
            if project / cpp != self.mainfile:
                self.libfiles.append(project / cpp)
        self.libfiles.extend(hs)
        self.libfiles.extend(hpps)
    
    def get_mainfile(self) -> str:
        assert self.mainfile is not None
        return self.mainfile.name.replace('\\', '/')
    
    def get_libfiles(self) -> List[str]:
        assert self.libfiles is not []
        libs = []
        for lib in self.libfiles:
            libs.append(lib.name.replace('\\', '/'))
        return libs

    def compile_project(self, compiler: Compiler):
        pass
