#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import sys
import time
import platform
import subprocess

from pathlib import Path

from lib_not_dr.nuitka import nuitka_config_type

from lib_not_dr.nuitka.reader.arg_parser import (
    pyproject_toml,
    toml_path_cli,
    gen_subprocess_args,
    subprocess_to_bash,
    parse_raw_config_by_script,
)

#  it will
# - read the given file or
# - find pyproject.toml in the given dir or
# - find pyproject.toml in current dir

# and read the `[tool.lndl.nuitka]` section
# then it will run nuitka with the given config

USEAGE = """
usage:
python lndl-nuitka.py --help (or -h)
show this help message

python lndl-nuitka.py <path-to-pyproject.toml>
python lndl-nuitka.py <path-to-dir>
python lndl-nuitka.py (with nothing, will use current dir)

arguments:
--no-run (-n) : only show the config, not run nuitka
--yes (-y) : run nuitka without asking
-- --xxx : pass to nuitka

用法:
python lndl-nuitka.py --help (或 -h)
显示这个帮助信息

python lndl-nuitka.py <一个文件>
python lndl-nuitka.py <一个路径>
python lndl-nuitka.py (直接运行 会使用当前目录)

参数:
--no-run (-n) : 只显示配置, 不运行 nuitka
--yes (-y) : 不询问直接运行 nuitka
-- --xxx : 传递给 nuitka 的参数

"""

TOML_READERS = (
    # "tomllib",  # stdlib toml reader after python 3.11
    # try tomllib first
    "toml",  # slow pure python toml reader
    "rtoml",  # rust based toml reader
    "tomli",  # pure python toml reader
    "pytomlpp",  # cpp based toml reader
    "qtoml",  # pure python toml reader, but faster than toml
    "tomlkit",  # pure python toml reader with style
)


def get_toml_reader():
    # 3.11 + 使用 tomllib
    if sys.version_info >= (3, 11):
        from tomllib import loads

        return loads
    for module_name in TOML_READERS:
        try:
            loaded = __import__(module_name).loads
            return loaded
        except ImportError:
            continue
    error_msg = """\033[31mNo toml reader found, please install any below by pip:
    {toml} or use Python 3.11+ or install lib-not-dr with lib_not_dr[nuitka] option
    没有找到 toml 解析器, 请考虑安装下列之一的 toml 库
    {toml} 或者使用 Python 3.11+ 或者使用 lib_not_dr[nuitka] 安装 lib-not-dr\033[0m
    """.format(toml="\n    ".join(TOML_READERS))
    raise ImportError(error_msg) from None


toml_loads = get_toml_reader()


def display_config(subprocess_command: list) -> None:
    print(f"The config is:\n\033[34m{subprocess_command} \033[0m")
    print("shell command is:\n\033[34m", end="")
    print(subprocess_to_bash(subprocess_command), "\033[0m")
    print(f"Working Dir: \033[32m {Path().cwd().absolute()} \033[0m")


def run_nuitka(subprocess_command: list) -> None:
    start_time = time.time()
    # shell true on windows
    # shell false on linux
    if platform.system() == "Windows":
        subprocess.run(subprocess_command, shell=True, check=True)
    else:
        subprocess.run(subprocess_command, shell=False, check=True)
    end_time = time.time()
    print(f"Time Elapsed: {end_time - start_time} seconds")


def main(config: nuitka_config_type) -> list:
    """
    enter point for python direct call
    :param config: nuitka config dict
    :return: None
    """
    subprocess_command = gen_subprocess_args(config)
    display_config(subprocess_command)
    return subprocess_command


def cli_main() -> None:
    """
    entering point of cli
    :return: None
    """
    if "--help" in sys.argv or "-h" in sys.argv:
        print(USEAGE)
        sys.exit(0)

    if len(sys.argv) < 2:
        print(USEAGE)
        if input("are you sure to run? (y/n)") not in ["y", "Y", "yes", "Yes"]:
            sys.exit(0)

    toml_file = toml_path_cli()

    with open(toml_file, "r", encoding="utf-8") as f:
        toml = toml_loads(f.read())

    nuitka_config = pyproject_toml(toml)
    cli_config = parse_raw_config_by_script(nuitka_config)

    subprocess_command = gen_subprocess_args(cli_config)
    display_config(subprocess_command)

    exit_arg = ("-no-run", "-n")
    confirm_arg = ("-y", "-yes")
    if any(arg in sys.argv for arg in exit_arg):
        sys.exit(0)
    elif all(arg not in sys.argv for arg in confirm_arg):
        if input("are you sure to run? (y/n)") not in ["y", "Y", "yes", "Yes"]:
            sys.exit(0)

    run_nuitka(subprocess_command)
