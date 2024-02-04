from xpinyin import Pinyin
from os import path


class CxxProject(object):
    CXX_EXT = ["cpp", "c", "hpp", "h"]

    def __init__(self, project_path: str, project_name: str = "", multifile: bool = False, ref: bool = False) -> None:
        print(project_path)
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
        self.ref: bool = ref
        self.multifile: bool = multifile
        self.score: int = 0

        # parse project info
        self.project_name = project_name
        self.author = self.project_path.split("/")[-1]

    def __str__(self) -> str:
        return """
        CxxProject
        project_path={},
        project_name={},
        author={},
        score={},
        ref={}
        """.format(self.project_path, self.project_name, self.author, self.score, self.ref)

    @property
    def is_multifile(self):
        return self.multifile
