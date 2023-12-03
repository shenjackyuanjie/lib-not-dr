#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time

from pathlib import Path
from types import FrameType
from typing import List, Optional, Tuple, Dict, Union

from lib_not_dr.types.options import Options

__all__ = ["LogMessage", "FormattingMessage"]


class LogMessage:
    # 消息内容本身的属性
    messages: List[str] = []
    end: str = "\n"
    split: str = " "

    # 消息的属性
    flush: Optional[bool] = None
    level: int = 20
    log_time: float = 0.0  # time.time_ns() if None
    logger_name: str = "root"
    logger_tag: Optional[str] = None
    stack_trace: Optional[FrameType] = None

    def __init__(
        self,
        messages: Optional[List[str]] = None,
        end: Optional[str] = "\n",
        split: Optional[str] = " ",
        flush: Optional[bool] = None,
        level: Optional[int] = 20,
        log_time: Optional[float] = None,
        logger_name: Optional[str] = "root",
        logger_tag: Optional[str] = None,
        stack_trace: Optional[FrameType] = None,
    ) -> None:
        """
        Init for LogMessage
        :param messages: message list for log
        :param end: end of message
        :param split: split for messages
        :param flush: do flush or not
        :param level: level of message
        :param log_time: time of message (default: time.time_ns())
        :param logger_name: name of logger
        :param logger_tag: tag of logger
        :param stack_trace: stack trace of logger
        """
        # 20231128 23:23
        # 因为 Options 的初始化太慢了 所以改为不继承 直接编写

        self.messages = messages if messages is not None else []
        self.end = end
        self.split = split
        self.level = level
        self.logger_name = logger_name
        self.logger_tag = logger_tag
        self.stack_trace = stack_trace

        if log_time is None:
            log_time = time.time_ns()
        self.log_time = log_time

        if not isinstance(flush, bool) and flush is not None:
            flush = True if flush else False
        self.flush = flush

    def option(self) -> Dict[str, Union[str, int, float, bool]]:
        return {
            "messages": self.messages,
            "end": self.end,
            "split": self.split,
            "flush": self.flush,
            "level": self.level,
            "log_time": self.log_time,
            "logger_name": self.logger_name,
            "logger_tag": self.logger_tag,
            "stack_trace": self.stack_trace,
        }

    def format_message(self) -> str:
        if self.split is None:
            self.split = " "
        return self.split.join(self.messages) + self.end

    def format_for_message(self) -> Dict[str, str]:
        basic_info = self.option()

        if self.logger_tag is None:
            basic_info["logger_tag"] = "   "

        basic_info["messages"] = self.format_message()

        return basic_info

    @property
    def create_msec_3(self) -> int:
        return int(self.log_time / 1000000) % 1000


FormattingMessage = Tuple[LogMessage, Dict[str, Union[str, Path]]]
