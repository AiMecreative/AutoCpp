import yaml
import argparse

from autocpp import CxxProject, Compiler


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

    cxx_project = CxxProject(
        project_path=args.project,
        project_name=configs[Compiler.COMPILER_KEY]["project_name"],
        multifile=args.multifile, ref=args.ref
    )

    compiler = Compiler(configs=configs[Compiler.COMPILER_KEY])
    compiler.config_cmake(cxx_project.project_path, cxx_project.multifile)
    compiler.cmake_build(cxx_project)
    compiler.cmake_run(cxx_project)
