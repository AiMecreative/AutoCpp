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
				if project.name == "readme.md": continue
				print(">>> config project: {} <<<".format(project.name))
				# config main file, use fool traversing 
				project = learner_folder / project
				if project.is_file():
					multifile = False
				if project.is_dir():
					multifile = True
				cproject = CProject(project, multifile)
				learner.append_task(cproject)
			learner_list.append(learner)
		return learner_list
	
	def config_workplace(self, options: Dict):
		Path.mkdir(self.build_folder, mode=711, parents=True, exist_ok=True)
		with Path.open(self.cmake_path, mode="w", encoding="utf-8") as cmake:
			cmake.write("cmake_minimum_required(VERSION {})\n".format(options["version"]))
			cmake.write("set(CMAKE_CXX_STANDARD {})\n".format(options["cxx_std"]))

	def check(self, learner: CLearner, ref: Path) -> None:
		for project in learner.task_list:
			with Path.open(self.cmake_path, mode="r", encoding="utf-8") as cmake:
				contents = cmake.readlines()[:2]
			contents.append("project({})\n".format(project.project_name))
			contents.append("add_executable({})\n".format(project.project_name))
			contents.append("target_sources({} PUBLIC {})\n".format(project.project_name, project.get_mainfile()))
			if project.is_multifile:
				contents.append("add_library({} {})\n".format(project.lib_name, " ".join(project.get_libfiles())))
				contents.append("target_link_libraries({} PUBLIC {})\n".format(project.project_name, " ".join(project.get_libfiles())))
			with Path.open(self.cmake_path, mode="w", encoding="utf-8") as cmake:
				cmake.writelines(contents)
