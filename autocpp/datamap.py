from typing import Dict
from dataclasses import dataclass, fields


@dataclass
class ConfigKey:

    _CompilerKey_: str = "CompilerKey"
    _CMakeKey_: str = "CMakeKey"


config_keys = ConfigKey()


@dataclass
class CompilerKey:

    _self_: str = ConfigKey._CompilerKey_
    CCompilerPath: str = "c_path"
    CXXCompilerPath: str = "cxx_path"
    BuildType: str = "build_type"
    BuildPath: str = "build_path"
    Generator: str = "generator"


@dataclass
class CompilerConfig:

    CCompilerPath: str
    CXXCompilerPath: str
    BuildType: str
    BuildPath: str
    Genrator: str


@dataclass
class CMakeKey:

    _self_: str = ConfigKey._CMakeKey_
    CMakePath: str = "cmake_path"
    CMakeMinVersion: str = "min_version"
    CXXStandard: str = "cxx_standard"
    ProjectName: str = "project_name"
    LibName: str = "lib_name"


@dataclass
class CMakeConfig:

    CMakePath: str
    CMakeMinVersion: float
    CXXStandard: int
    ProjectName: str
    LibName: str


def config_parse(config: dict) -> Dict:
    config_dict = {}
    keys = config.keys()
    for k in keys:
        # k is the class name
        key_instance = globals()[k]()
        data_instance = globals()[k.replace("Key", "Config")]()
        k_config = config[k]
        for ak in fields(key_instance):
            attr_key = getattr(key_instance, ak.name)
            if attr_key == k:
                continue
            setattr(data_instance, ak.name, k_config[attr_key])
        config_dict[k] = data_instance
    return config_dict
