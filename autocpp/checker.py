import shutil
import re
from typing import List, Dict
from pathlib import Path
from autocpp import CLearner, CProject


class Checker(object):

	def __init__(self, checker_path: Path) -> None:
		self.workplace = checker_path
		self.build_folder = self.workplace / "build"
		self.cmake_path = self.workplace / "CMakeLists.txt"
		self.mainfile: Path = None

	def create_workfolder(self, tasks_root_folder: Path, task_prefix: str="task") -> None:
		Path.mkdir(self.workplace, mode=711, parents=True, exist_ok=True)
		# find all learners' task folder
		tasks_list = tasks_root_folder.iterdir()
		for t_idx, tasks in enumerate(tasks_list):
			# tasks is the dir name of one learner, copy to new working dir and rename it
			work_folder = self.workplace / (f"{task_prefix}{t_idx}")
			Path.mkdir(work_folder, mode=711, parents=True, exist_ok=True)
			with Path.open(work_folder / "readme.md", mode="w", encoding="utf-8") as info:
				info.write("tasks_name: " + tasks.name)
			# copy all projects files into new working folder
			projects_list = tasks.iterdir()
			for p_idx, project in enumerate(projects_list):
				dst_name = f"question{p_idx}"
				if project.is_file():
					dst_name += ".cpp"
					shutil.copyfile(tasks_root_folder / tasks / project, work_folder / dst_name)
				if project.is_dir():
					shutil.copytree(tasks_root_folder / tasks / project, work_folder / dst_name, dirs_exist_ok=True)
	
	def config_learner(self) -> List[CLearner]:
		learner_list = []
		folders = self.workplace.iterdir()
		for learner_folder in folders:
			print(">>>--- config learner: {} ---<<<".format(learner_folder.name))
			if learner_folder.is_file() or learner_folder.name == "build":
				continue
			learner_folder = self.workplace / learner_folder
			learner = CLearner(learner_folder)
			projects = learner_folder.iterdir()
			for project in projects:
				print(">>> config project: {} <<<".format(project.name))
				# config main file, use fool traversing 
				cproject = None
				project = learner_folder / project
				if project.is_file():
					cproject = CProject(project, multifile=False)
				if project.is_dir():
					# open every cpp file in order and match the `main` function
					# self.find_mainfile(project)
					cproject = CProject(project, multifile=True)
				# cproject.config_mainfile()
				# cproject.config_libfiles()
				learner.append_task(cproject)
			learner_list.append(learner)
		return learner_list
	
	def config_workplace(self, options: Dict):
		Path.mkdir(self.build_folder, mode=711, parents=True, exist_ok=True)
		with Path.open(self.cmake_path, mode="w", encoding="utf-8") as cmake:
			cmake.write("cmake_minimum_required(VERSION {})".format(options["version"]))
			cmake.write("set(CMAKE_CXX_STANDARD {})".format(options["cxx_std"]))

	def check(self, learner: CLearner, ref: Path) -> None:
		for project in learner.task_list:
			with Path.open(self.cmake_path, mode="r", encoding="utf-8") as cmake:
				contents = cmake.readlines()
			contents.append("project({})".format(project.project_name))
			if project.is_multifile:
				contents.append("add_library({} {})".format(project.lib_name, " ".join(project.get_libfiles())))
			contents.append("add_execuable({})".format(project.project_name))
			contents.append("target_sources({} PUBLIC {})".format(project.project_name, project.get_mainfile()))
			contents.append("target_link_libraries({} PUBLIC {})".format(project.project_name, " ".join(project.get_libfiles())))
			with Path.open(self.cmake_path, mode="w", encoding="utf-8") as cmake:
				cmake.writelines(contents)
