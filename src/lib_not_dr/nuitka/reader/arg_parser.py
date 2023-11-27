#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys

from pathlib import Path
from warnings import warn
from typing import Iterable, Dict, Union, List


def pyproject_toml(toml_data: dict) -> dict:
    """
    :param toml_data: dict (from pyproject/ raw dict)
    :return: dict
    """
    if "tool" not in toml_data:
        raise ValueError("No tool section in config file/dict")

    if "lndl" not in toml_data["tool"]:
        raise ValueError("No lib-not-dr(lndl) section in config file/dict")

    if "nuitka" not in toml_data["tool"]["lndl"]:
        raise ValueError("No lib-not-dr(lndl).nuitka section in config file/dict")

    nuitka_config = toml_data["tool"]["lndl"]["nuitka"]

    if "main" not in nuitka_config:
        raise ValueError(
            "'main' not define in lib-not-dr(lndl).nuitka section\ndefine it with 'main = [<main.py>]'"
        )

    return nuitka_config


def toml_path_cli() -> Path:
    """
    get toml path from cli args
    :return: Path
    """
    if len(sys.argv) < 2:
        raw_path = Path().cwd()
    else:
        raw_path = Path(sys.argv[1])
    if raw_path.is_file():
        return raw_path

    elif raw_path.is_dir():
        if (raw_path / "pyproject.toml").exists():
            return raw_path / "pyproject.toml"
        else:
            raise FileNotFoundError(f"pyproject.toml not found in {raw_path}")
    else:
        raise FileNotFoundError(f"{raw_path} not found")


def get_cli_nuitka_args() -> dict:
    """
    get -- from sys.argv
    :return: list
    """
    # no -- in sys.argv
    if len(sys.argv) < 2:
        return {}
    if '--' not in sys.argv:
        return {}

    # start from --
    index = sys.argv.index('--')
    new_args = sys.argv[index + 1:]
    arg_dict = {}
    for arg in new_args:
        if not arg.startswith('--'):
            warn(f"invalid arg: {arg}")
        else:
            arg = arg[2:]  # remove --
            # arg_name: --<name>=<value>
        arg_name = arg.split('=')[0]
        if '=' in arg:
            arg_value = arg.split('=')[1]
        else:
            arg_value = True
        arg_dict[arg_name] = arg_value

    print(f"cli config: {arg_dict}")
    return arg_dict


def merge_cli_config(toml_config: dict, cli_config: dict) -> dict:
    """
    merge toml config and cli config
    :param toml_config:
    :param cli_config:
    :return:
    """
    for name, value in cli_config.items():
        if name in toml_config:
            warn(f"\033[33mcli config will overwrite toml config\n{name}:{toml_config[name]} -> {value}\033[0m")
            if isinstance(toml_config[name], bool):
                if not isinstance(value, bool):
                    warn(f"cli config {name} is bool but toml config is not\n{value} -> {value}")
                    continue
                toml_config[name] = value
            elif isinstance(toml_config[name], str):
                if not isinstance(value, str):
                    warn(f"cli config {name} is str but toml config is not\n{value} -> {value}")
                    continue
                toml_config[name] = value
            elif isinstance(toml_config[name], Iterable):
                if not isinstance(value, str):
                    warn(f"cli config {name} is Iterable but toml config is not\n{value} -> {value}")
                    continue
                toml_config[name].append(value)
        else:
            toml_config[name] = value
    return toml_config


def gen_subprocess_args(nuitka_config:
                        Dict[str, Union[str, bool, List[Union[str, tuple]]]]) -> list:
    cmd_list = [sys.executable, "-m", "nuitka"]

    nuitka_config = merge_cli_config(nuitka_config, get_cli_nuitka_args())

    def parse_value(arg_name, arg_value) -> list:
        if isinstance(value, bool):
            warn(f"bool value is not supported in list config {arg_name}")
            return []
        elif isinstance(value, str):
            return [f"--{arg_name}={arg_value}"]
        else:
            return [f"--{arg_name}={arg_value[0]}={arg_value[1]}"]

    for name, value in nuitka_config.items():
        if value is True:
            # --<name>
            cmd_list.append(f"--{name}")
            continue
        elif isinstance(value, str):
            # --<name>=<value>
            cmd_list.append(f"--{name}={value}")
            continue
        elif isinstance(value, Iterable):
            if '__spilt__' in value:
                # --<name>=<value1> --<name>=<value2> ...
                for item in value:
                    if item == '__spilt__':
                        continue
                    cmd_list += parse_value(name, item)
                continue
            if all(isinstance(item, str) for item in value):
                # --<name>=<value1>,<value2>,...
                cmd_list.append(f"--{name}={','.join(value)}") # type: ignore
            elif all(isinstance(item, (tuple, list)) for item in value):
                # --<name>=<value1>=<value2>
                # --<name>=<value3>=<value4>,...
                for item in value:
                    cmd_list.append(f"--{name}={item[0]}={item[1]}")
            else:
                # 处理混杂的情况
                for item in value:
                    cmd_list += parse_value(name, item)
                continue

    return cmd_list


def subprocess_to_bash(cmd_list: List[str]) -> str:
    """
    :param cmd_list: list
    :return: str
    """
    cmd_list = [item if ' ' not in item else f'"{item}"' for item in cmd_list]
    return " ".join(cmd_list)
