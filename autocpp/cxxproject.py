from xpinyin import Pinyin
from os import path


class CxxProject(object):
    """config cpp projects, extract info from given path"""
    CXX_EXT = ["cpp", "c", "hpp", "h"]

    def __init__(self, project_path: str, multifile: bool = False, ref: bool = False) -> None:
        if project_path is None or "":
            raise Exception("project_path is none or empty")
        if not path.exists(project_path):
            raise Exception("project_path is not exists")
        if not multifile:
            if path.splitext[1] not in self.CXX_EXT:
                raise Exception("project_path not points to a cxx project")
        if multifile:
            if not path.isdir(project_path):
                raise Exception("project_path should points to a cxx project folder in multi-file mode")

        self.project_path: str = project_path.replace("\\", "/")
        self.multifile: bool = multifile
        self.ref: bool = ref
        
        self.main_file: str = ""

        # parse project info
        self.score: int = 0

    def __str__(self) -> str:
        return """
        CxxProject
        project_path={},
        score={},
        ref={}
        """.format(self.project_path, self.score, self.ref)

    @property
    def is_multifile(self):
        return self.multifile

    @property
    def is_ref(self):
        return self.ref

    def config_score(self, given_score: int):
        self.score = given_score
