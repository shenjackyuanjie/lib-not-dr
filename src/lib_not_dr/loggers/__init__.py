#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import sys

from typing import Dict, TYPE_CHECKING

from lib_not_dr.types.options import Options

COLOR_SUPPORT = True

if sys.platform == "win32":
    try:
        # https://stackoverflow.com/questions/36760127/...
        # how-to-use-the-new-support-for-ansi-escape-sequences-in-the-windows-10-console
        from ctypes import windll

        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except OSError:  # pragma: no cover
        COLOR_SUPPORT = False


class LogLevel(Options):
    name = "LogLevel"
    notset: int = 0
    notset_name: str = "NOTSET"
    trace: int = 5
    trace_name: str = "TRACE"
    fine: int = 7
    fine_name: str = "FINE"
    debug: int = 10
    debug_name: str = "DEBUG"
    info: int = 20
    info_name: str = "INFO"
    warn: int = 30
    warn_name: str = "WARN"
    error: int = 40
    error_name: str = "ERROR"
    fatal: int = 50
    fatal_name: str = "FATAL"

    level_name_map: Dict[int, str] = {
        notset: notset_name,
        trace:  trace_name,
        fine:   fine_name,
        debug:  debug_name,
        info:   info_name,
        warn:   warn_name,
        error:  error_name,
        fatal:  fatal_name,
    }

    name_level_map: Dict[str, int] = {
        notset_name: notset,
        trace_name:  trace,
        fine_name:   fine,
        debug_name:  debug,
        info_name:   info,
        warn_name:   warn,
        error_name:  error,
        fatal_name:  fatal,
    }

    @classmethod
    def parse_name_level(cls, name: str) -> int:
        """
        parse logging name to level int
        :param name: logging level name
        """
        name = name.upper()
        if name in cls.name_level_map:
            return cls.name_level_map[name]
        else:
            return cls.notset

    @classmethod
    def parse_level_name(cls, level_int: int, use_upper: bool = True) -> str:
        """
        parse logging level int to name
        :param level_int: logging level int
        :param use_upper:
        """
        if (result := cls.level_name_map.get(level_int)) is not None:
            return result

        if use_upper:
            for level in cls.level_name_map:
                if level_int <= level:
                    return cls.level_name_map[level]
        else:
            for level in reversed(cls.level_name_map):
                if level_int >= level:
                    return cls.level_name_map[level]
        return cls.notset_name


# fmt: off
from lib_not_dr.loggers.config import get_logger, get_config, read_config  # noqa: E402

if TYPE_CHECKING:
    from lib_not_dr.loggers import logger
    from lib_not_dr.loggers import formatter
    from lib_not_dr.loggers import outstream
    from lib_not_dr.loggers import structure
    from lib_not_dr.loggers import config

__all__ = [
    # modules
    'logger',
    'formatter',
    'outstream',
    'structure',
    'config',
    # class
    'LogLevel',
    # function,
    'get_logger',
    'get_config',
    'read_config',
    # variable
    'COLOR_SUPPORT',
]
# fmt: on
