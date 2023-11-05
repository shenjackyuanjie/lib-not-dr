#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import inspect
from types import FrameType
from typing import List, Optional

from lib_not_dr.logger.structure import LogMessage
from lib_not_dr.logger.outstream import BaseOutputStream
from lib_not_dr.types.options import Options


class Logger(Options):
    name = 'Logger-v2'

    outputs: List[BaseOutputStream] = []

    enable: bool = True
    level: int = 20

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

        Args:
            output (BaseOutputStream): The output to be added.

        Returns:
            None
        """
        self.outputs.append(output)
        self.level = min(self.level, output.level)

    def remove_output(self, output: BaseOutputStream) -> None:
        """
        Removes the specified output from the list of outputs.

        Args:
            output (BaseOutputStream): The output to be removed.

        Returns:
            None
        """
        self.outputs.remove(output)
        self.level = max(self.level, *[output.level for output in self.outputs])

    def make_log(self,
                 messages: List[str],
                 end: str = '\n',
                 split: str = ' ',
                 flush: bool = True,
                 level: int = 20,
                 log_time: Optional[float] = None,
                 logger_name: str = 'root',
                 logger_tag: Optional[str] = None,
                 stack_trace: Optional[FrameType] = None) -> None:
        # 检查是否需要记录
        if not self.log_for(level):
            return
        # 处理时间
        if log_time is None:
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

        message = LogMessage(messages=messages,
                             end=end,
                             split=split,
                             flush=flush,
                             level=level,
                             log_time=log_time,
                             logger_name=logger_name,
                             logger_tag=logger_tag,
                             stack_trace=stack_trace)
