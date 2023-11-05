#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys

from lib_not_dr.types.options import Options
from lib_not_dr.logger.structure import LogMessage
from lib_not_dr.logger.formatter import BaseFormatter, StdFormatter

__all__ = [
    'BaseOutputStream'
]


class BaseOutputStream(Options):
    name = 'BaseOutputStream'

    level: int = 20
    enable: bool = True

    formatter: BaseFormatter

    def write_stdout(self, message: LogMessage) -> None:
        raise NotImplementedError(f'{self.__class__.__name__}.write_stdout is not implemented')

    def write_stderr(self, message: LogMessage) -> None:
        raise NotImplementedError(f'{self.__class__.__name__}.write_stderr is not implemented')

    def flush(self) -> None:
        raise NotImplementedError(f'{self.__class__.__name__}.flush is not implemented')


class StdioOutputStream(BaseOutputStream):
    name = 'StdioOutputStream'

    formatter: BaseFormatter = StdFormatter()

    def write_stdout(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        print(self.formatter.format_message(message), end='', flush=message.flush)
        return None

    def write_stderr(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        print(self.formatter.format_message(message), end='', flush=message.flush, file=sys.stderr)
        return None

    def flush(self) -> None:
        """
        flush stdout and stderr
        :return: None
        """
        print('', end='', flush=True)
        print('', end='', flush=True, file=sys.stderr)
        return None


class FileCacheOutputStream(BaseOutputStream):
    name = 'FileCacheOutputStream'

    formatter: BaseFormatter = StdFormatter(enable_color=False)