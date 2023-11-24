#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import sys
import time
import subprocess

from pathlib import Path
from typing import Iterable

USEAGE = """
usage:
python lndl-nuitka.py --help (or -h)
show this help message

python lndl-nuitka.py <path-to-pyproject.toml>
python lndl-nuitka.py <path-to-dir>
python lndl-nuitka.py (with nothing, will use current dir)

then it will
- read the given file or
- find pyproject.toml in the given dir or
- find pyproject.toml in current dir

and read the `[tool.lndl.nuitka]` section

then it will run nuitka with the given config

用法:
python lndl-nuitka.py --help (或 -h)
显示这个帮助信息

python lndl-nuitka.py <一个文件>
python lndl-nuitka.py <一个路径>
python lndl-nuitka.py (直接运行 会使用当前目录)

然后它会
- 读取给定的文件 或
- 在给定的路径中找到 pyproject.toml 或
- 在当前目录中找到 pyproject.toml

并读取 `[tool.lndl.nuitka]` 部分

然后它会使用给定的配置运行 nuitka
"""

TOML_READERS = (
    "tomllib",  # stdlib toml reader after python 3.11
    "toml",  # slow pure python toml reader
    "rtoml",  # rust based toml reader
    "tomlkit",  # pure python toml reader
    "tomli",  # pure python toml reader
    "pytomlpp",  # cpp based toml reader
    "qtoml",  # pure python toml reader, but faster than toml
)


def get_toml_reader():
    for module_name in TOML_READERS:
        try:
            toml_loads = __import__(module_name).loads
            return toml_loads
        except ImportError:
            continue
    error_msg = """No toml reader found, please install any below by pip:\n%s
    or use Python 3.11+""" % " ".join(
        TOML_READERS
    )
    raise ImportError(error_msg) from None


toml_loads = get_toml_reader()


def validate_toml(toml_data: dict, file_name: Path) -> dict:
    if "tool" not in toml_data:
        raise ValueError(f"No tool section in {file_name}")

    if "lndl" not in toml_data["tool"]:
        raise ValueError(f"No lib-not-dr(lndl) section in {file_name}")

    if "nuitka" not in toml_data["tool"]["lndl"]:
        raise ValueError(f"No lib-not-dr(lndl).nuitka section in {file_name}")

    nuitka_config = toml_data["tool"]["lndl"]["nuitka"]

    if "main" not in nuitka_config:
        raise ValueError(
            "'main' not define in lib-not-dr(lndl).nuitka section\ndefine it with 'main = [<main.py>]'"
        )

    return nuitka_config


def gen_subprocess_args(nuitka_config: dict) -> list:
    cmd_list = [sys.executable, "-m", "nuitka"]

    for name, value in nuitka_config.items():
        if value is True:
            # --<name>
            cmd_list.append("--%s" % name)
            continue
        elif isinstance(value, str):
            # --<name>=<value>
            cmd_list.append("--%s=%s" % (name, value))
            continue
        elif isinstance(value, Iterable):
            # --<name>=<value1>,<value2>,...
            cmd_list.append("--%s=%s" % (name, ",".join(value)))
            continue

    return cmd_list


def get_toml() -> Path:
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


def main():
    toml_file = get_toml()

    with open(toml_file, "r", encoding="utf-8") as f:
        toml = toml_loads(f.read())

    nuitka_config = validate_toml(toml, toml_file)

    subprocess_command = gen_subprocess_args(nuitka_config)

    # printed in blue text
    # \033[34m is the escape code for blue text
    print(f"\033[34mRunning: {subprocess_command}\033[0m")

    start_time = time.time()
    subprocess.run(subprocess_command, shell=True)
    end_time = time.time()

    print(f"Time Elapsed: {end_time - start_time} seconds")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(USEAGE)
        sys.exit(0)
    if len(sys.argv) < 2:
        print(USEAGE)
        if input("are you sure to run? (y/n)") not in ["y", "Y", "yes", "Yes"]:
            sys.exit(0)
    main()
