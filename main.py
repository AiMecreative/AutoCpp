from autocpp import CLearner, Compiler, CProject
from pathlib import Path


tasks_root = Path("data")
ref_root = Path("ref")
spliter = '\\'

if __name__ == "__main__":
    tasks_list = tasks_root.iterdir()
    for tasks in tasks_list:

        learner = CLearner(tasks.name.split(spliter)[-1], tasks)
