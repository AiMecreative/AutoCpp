from autocpp import Compiler


class CProject(object):

    def __init__(self, project_path: str, mainfile: str, multifile: bool,
                 project_name: str = "task", lib_name: str = "tasklib") -> None:
        self.project_path: str = project_path
        self.mainfile: str = mainfile
        self.multifile: bool = multifile
        self.project_name: str = project_name
        self.lib_name: str = lib_name
        self.score: float = 0.

    def compile_project(self, compiler: Compiler):
        pass
