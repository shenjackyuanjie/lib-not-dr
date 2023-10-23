#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time

from types import FrameType
from typing import List, Optional, Tuple, Dict

from lib_not_dr.types.options import Options

__all__ = ['LogMessage',
           'FormattingMessage']


class LogMessage(Options):
    name = 'LogMessage'

    # 消息内容本身的属性
    messages: List[str] = []
    end: str = '\n'
    split: str = ' '

    # 消息的属性
    flush: bool = True
    level: int = 20
    log_time: float = None  # time.time_ns()
    logger_name: str = 'root'
    logger_tag: Optional[str] = None
    stack_trace: Optional[FrameType] = None

    def init(self, **kwargs) -> bool:
        if self.log_time is None:
            self.log_time = time.time_ns()
        return False

    def format_message(self) -> str:
        return self.split.join(self.messages) + self.end

    def format_for_message(self) -> Dict[str, str]:
        basic_info = self.option()

        if self.logger_tag is None:
            basic_info['logger_tag'] = '   '

        basic_info['messages'] = self.format_message()

        return basic_info

    @property
    def create_msec_3(self) -> int:
        return int(self.log_time / 1000000) % 1000


FormattingMessage = Tuple[LogMessage, Dict[str, str]]
