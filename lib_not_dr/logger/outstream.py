#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import io
import sys
import time
import string
import atexit
import threading

from pathlib import Path

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

    def close(self) -> None:
        self.enable = False


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

    text_cache: io.StringIO = None

    flush_counter: int = 0
    # 默认 10 次 flush 一次
    flush_count_limit: int = 10
    flush_lock: threading.Lock = None

    file_path: Path = Path('./logs')
    file_name: str
    # file mode: always 'rw'
    file_encoding: str = 'utf-8'
    # do file swap or not
    file_swap: bool = False

    file_swap_counter: int = 0
    file_swap_name_template: str = '${name}-${counter}.log'
    # ${name} -> file_name
    # ${counter} -> file_swap_counter
    # ${log_time} -> time when file swap ( round(time.time()) )
    # ${start_time} -> start time of output stream ( round(time.time()) )
    current_file_name: str = None
    file_start_time: int = None

    # log file swap triggers
    # 0 -> no limit
    file_size_limit: int = 0  # size limit in kb
    file_time_limit: int = 0  # time limit in sec 0
    file_swap_on_both: bool = False  # swap file when both size and time limit reached

    def init(self, **kwargs) -> bool:
        if self.text_cache is None:
            # ( 其实我也不确定为啥这么写 反正按照 "规范" 来说, StringIO 算是 "file" )
            return True
        self.flush_lock = threading.Lock()
        return False

    def load_file(self) -> bool:
        self.file_start_time = round(time.time())
        if self.text_cache is None:
            self.text_cache = io.StringIO()
        return True

    def _write(self, message: LogMessage) -> None:
        """
        write message to text cache
        默认已经检查过了
        :param message: message to write
        :return: None
        """
        self.text_cache.write(self.formatter.format_message(message))
        self.flush_counter += 1
        if message.flush or self.flush_counter >= self.flush_count_limit:
            self.flush()
        else:
            atexit.register(self.flush)
        return None

    def write_stdout(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        self._write(message)
        return None

    def write_stderr(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        self._write(message)
        return None

    def get_file_path(self) -> Path:
        """
        get file path
        :return:
        """
        if (current_file := self.current_file_name) is None:
            if self.file_start_time is None:
                self.file_start_time = round(time.time())
            template = string.Template(self.file_swap_name_template)
            file_name = template.safe_substitute(name=self.file_name,
                                                 counter=self.file_swap_counter,
                                                 log_time=round(time.time()),
                                                 start_time=self.file_start_time)
            current_file = Path(self.file_path) / file_name
            self.current_file_name = str(current_file.absolute())
        else:
            current_file = Path(current_file)
        return current_file

    def check_flush(self) -> Path:
        current_file = self.get_file_path()
        # 获取当前文件的路径
        if not self.file_swap:
            # 不需要 swap 直接返回
            return current_file
        # 检查是否需要 swap
        size_pass = True
        if self.file_size_limit > 0:
            file_size = current_file.stat().st_size / 1024  # kb
            if file_size > self.file_size_limit:  # kb
                size_pass = False
        time_pass = True
        if self.file_time_limit > 0:
            file_time = round(time.time()) - current_file.stat().st_mtime
            if file_time > self.file_time_limit:
                time_pass = False
        if (self.file_swap_on_both and size_pass and time_pass) or \
           (not self.file_swap_on_both and (size_pass or time_pass)):
            # 两个都满足
            # 或者只有一个满足
            if size_pass and time_pass:
                self.file_swap_counter += 1
                # 生成新的文件名
                return self.get_file_path()

    def flush(self) -> None:
        new_cache = io.StringIO()  # 创建新的缓存
        self.flush_counter = 0  # atomic, no lock
        with self.flush_lock:
            text = self.text_cache.getvalue()
            old_cache, self.text_cache = self.text_cache, new_cache
        old_cache.close()  # 关闭旧的缓存
        if text == '':
            return None
        current_file = self.check_flush()

    def close(self) -> None:
        super().close()
        self.flush()
        self.text_cache.close()
        atexit.unregister(self.flush)
        return None
