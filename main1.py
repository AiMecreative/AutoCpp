import yaml
import argparse

from autocpp1 import CxxProject, Compiler, config_parse


config_path = "./config.yml"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=str, help="the folder or file of cxx project")
    parser.add_argument("--config", type=str, default=config_path, help="the config file path")
    parser.add_argument("--multifile", action="store_true", default=False, help="if project is multifile")
    parser.add_argument("--ref", action="store_true", default=False, help="if the project is reference")

    args = parser.parse_args()
    with open(args.config, "r") as y:
        configs = yaml.safe_load(y)
        configs = config_parse(configs)

    cxx_project = CxxProject(
        project_path=args.project,
        multifile=args.multifile, ref=args.ref)
    work_path = cxx_project.project_path
    
    compiler = Compiler(configs=configs)
    compiler.cmake_init(cxx_project)
    compiler.run("config", work_path)
    compiler.run("build", work_path)
    compiler.run("run", work_path)
