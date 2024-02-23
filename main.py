import re

from autocpp import CLearner, Compiler, CProject, Checker
from pathlib import Path


current_path = Path.cwd()
tasks_root = current_path / Path("data")
working_root = current_path / Path("working")
ref_root = current_path / Path("ref")

cmake_opt = {
    "version": 3.22,
    "cxx_std": 17
}


if __name__ == "__main__":
    checker_path = working_root
    checker = Checker(checker_path)
    checker.create_workfolder(tasks_root)
    learners = checker.config_learner()
    for learner in learners:
        checker.config_workplace(cmake_opt)
        checker.check(learner, ref=Path(""))
    
        
