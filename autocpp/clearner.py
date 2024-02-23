from autocpp import CProject
from typing import List
from pathlib import Path


class CLearner(object):

    def __init__(self, name: str, folder: Path, task_list: List[CProject]=None) -> None:
        self.name: str = name
        self.task_list: List[CProject] = task_list
        self.folder: Path = folder
        self.scores: List[float] = []
    
    def append_task(self, task: CProject):
        self.task_list.append(task)
