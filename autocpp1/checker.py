from .compiler import Compiler
from .cxxproject import CxxProject
from typing import List, Dict


class AutoChecker(object):

    def __init__(self, task_name: str, compiler: Compiler) -> None:
        self.task_name = task_name
        self.compiler: Compiler = compiler

        # problem No.: pair(test_samples, test_results)
        self.references: Dict = {}

    def give_score(self): pass

    def add_ref(self, ref_project: CxxProject, test_samples: List):
        pass

    def check(self, cxx_project: CxxProject, test_samples: List):
        pass
