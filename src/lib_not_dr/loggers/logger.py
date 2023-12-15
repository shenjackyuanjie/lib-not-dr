#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import inspect
from types import FrameType
from typing import List, Optional, Union

from lib_not_dr.loggers import LogLevel
from lib_not_dr.types.options import Options
from lib_not_dr.loggers.structure import LogMessage
from lib_not_dr.loggers.outstream import BaseOutputStream, StdioOutputStream


class Logger(Options):
    name = "Logger-v2"

    outputs: List[BaseOutputStream] = [StdioOutputStream()]

    logger_name: str = "root"
    default_tag: Optional[str] = None

    enable: bool = True
    level: int = 20  # info

    def clone_logger(self) -> "Logger":
        """
        Clone a new loggers with the same config.

        Returns:
            Logger: The cloned loggers.
        """
        return Logger(
            logger_name=self.logger_name,
            enable=self.enable,
            level=self.level,
            outputs=self.outputs.copy(),
            default_tag=self.default_tag,
        )

    def log_for(self, level: int) -> bool:
        """
        Check if logging is enabled for a specific level.

        Args:
            level (int): The logging level to check.

        Returns:
            bool: True if logging is enabled for the given level, False otherwise.
        """
        return self.enable and level >= self.level

    def add_output(self, output: BaseOutputStream) -> None:
        """
        Add an output to the list of outputs.
        :param output:
        :return:
        """
        self.outputs.append(output)
        self.level = min(self.level, output.level)

    def remove_output(self, output: BaseOutputStream) -> None:
        """
        Remove an output from the list of outputs.
        :param output: BaseOutputStream
        :return:
        """
        self.outputs.remove(output)
        self.level = max(self.level, *[output.level for output in self.outputs])

    @property
    def tag(self):
        """
        Get the default tag.
        :return:
        """
        return self.default_tag

    @tag.setter
    def tag(self, tag: str) -> None:
        """
        Set the default tag.
        :param tag: str
        :return: None
        """
        self.default_tag = tag

    def set_tag(self, tag: str) -> "Logger":
        """
        Set the default tag.
        :param tag: str
        :return: None
        """
        self.default_tag = tag
        return self

    def clear_tag(self) -> None:
        """
        Clear the default tag.
        :return:
        """
        self.default_tag = None

    @property
    def global_level(self) -> int:
        """
        Get the global logging level.

        Returns:
            int: The global logging level.
        """
        return self.level

    @global_level.setter
    def global_level(self, level: int) -> None:
        """
        Set the global logging level.

        Args:
            level (int): The global logging level.

        Returns:
            None
        """
        self.level = level
        for output in self.outputs:
            output.level = level

    def make_log(
            self,
            messages: Union[list, tuple],
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            level: int = 20,  # info
            # log_time: Optional[float] = None,
            # logger_name: str = 'root',
            # logger_tag: Optional[str] = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        # 检查是否需要记录
        if not self.log_for(level):
            return
        log_time = time.time_ns()
        # 处理堆栈信息
        if stack_trace is None:
            # 尝试获取堆栈信息
            if (stack := inspect.currentframe()) is not None:
                # 如果可能 尝试获取上两层的堆栈信息
                if (up_stack := stack.f_back) is not None:
                    if (upper_stack := up_stack.f_back) is not None:
                        stack_trace = upper_stack
                    else:
                        stack_trace = up_stack
                else:
                    stack_trace = stack
        # 处理标签
        if tag is None and self.default_tag is not None:
            tag = self.default_tag

        message = LogMessage(
            messages=messages,  # type: ignore
            end=end,
            split=split,
            flush=flush,
            level=level,
            log_time=log_time,
            logger_name=self.logger_name,
            logger_tag=tag,
            stack_trace=stack_trace,
        )
        if level >= 30:  # WARN
            for output in self.outputs:
                output.write_stderr(message)
        else:
            for output in self.outputs:
                output.write_stdout(message)
        # done?
        # 20231106 00:06

    def info(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.info):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.info,
            stack_trace=stack_trace,
        )

    def trace(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.trace):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.trace,
            stack_trace=stack_trace,
        )

    def fine(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.fine):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.fine,
            stack_trace=stack_trace,
        )

    def debug(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.debug):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.debug,
            stack_trace=stack_trace,
        )

    def warn(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.warn):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.warn,
            stack_trace=stack_trace,
        )

    def error(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.error):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.error,
            stack_trace=stack_trace,
        )

    def fatal(
            self,
            *message,
            tag: Optional[str] = None,
            end: str = "\n",
            split: str = " ",
            flush: bool = None,
            stack_trace: Optional[FrameType] = None,
    ) -> None:
        if not self.log_for(LogLevel.fatal):
            return
        self.make_log(
            messages=message,
            tag=tag,
            end=end,
            split=split,
            flush=flush,
            level=LogLevel.fatal,
            stack_trace=stack_trace,
        )
