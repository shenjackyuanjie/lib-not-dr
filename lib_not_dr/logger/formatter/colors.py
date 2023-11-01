#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Dict, Tuple

from lib_not_dr.logger.formatter import BaseFormatter
from lib_not_dr.logger.structers import FormattingMessage


__all__ = [
    'BaseColorFormatter',
    'LevelColorFormatter',
    'LoggerColorFormatter',
    'RESET_COLOR'
]

RESET_COLOR = '\033[0m'


class BaseColorFormatter(BaseFormatter):
    name = 'BaseColorFormatter'

    @staticmethod
    def _default_color() -> Dict[int, str]:
        return {
            # Notset: just black
            0: '',
            # Trace: blue
            2: '\033[0;34m',
            # Fine: green
            5: '\033[0;32m',
            # Debug: cyan
            7: '\033[0;36m',
            # Info: white
            10: '\033[0;37m',
            # Warn: yellow
            30: '\033[0;33m',
            # Error: red
            50: '\033[0;31m',
            # Fatal: red background
            90: '\033[0;41m'
        }

    @staticmethod
    def get_level(message: FormattingMessage, colors: Dict[int, str] = None) -> int:
        if colors is None:
            colors = BaseColorFormatter._default_color()
        for level in colors:
            if message[0].level < level:
                break
        else:
            level = 90
        return level


class LevelColorFormatter(BaseColorFormatter):
    name = 'LevelColorFormatter'

    @staticmethod
    def _default_color() -> Dict[int, str]:
        return {
            # Notset: just black
            0: '',
            # Trace: blue
            2: '\033[0;34m',
            # Fine: green
            5: '\033[0;32m',
            # Debug: cyan
            7: '\033[0;36m',
            # Info: white
            10: '\033[0;37m',
            # Warn: yellow
            30: '\033[0;33m',
            # Error: red
            50: '\033[0;31m',
            # Fatal: red background
            90: '\033[0;41m'
        }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('colored level', 'level', 'A colored level')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if isinstance(message[1].get('level'), int):
            return message
        # 向上寻找等级
        level = self.get_level(message, self._default_color())
        # 获取颜色
        color = self._default_color()[level]
        # 添加颜色
        message[1]['level'] = f'{color}{message[1]["level"]}{RESET_COLOR}'
        return message


class LoggerColorFormatter(BaseColorFormatter):
    name = 'LoggerColorFormatter'

    @staticmethod
    def _default_color() -> Dict[int, str]:
        return {
            # Notset: just black
            0: '',
            # Trace: blue
            2: '\033[0;34m',
            # Fine: green
            5: '\033[0;32m',
            # Debug: cyan
            7: '\033[0;36m',
            # Info: white
            10: '\033[0;37m',
            # Warn: yellow
            30: '\033[0;33m',
            # Error: red
            50: '\033[0;31m',
            # Fatal: red background
            90: '\033[0;41m',
        }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('colored logger name', 'logger name', 'A colored logger name')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[1].get('logger_name') is None:
            return message
        # 向上寻找等级
        level = self.get_level(message, self._default_color())
        # 获取颜色
        color = self._default_color()[level]
        # 添加颜色
        message[1]['logger_name'] = f'{color}{message[1]["logger_name"]}{RESET_COLOR}'
        if message[1].get('logger_tag') is not None and message[1].get('logger_tag') != '   ':
            message[1]['logger_tag'] = f'{color}{message[1]["logger_tag"]}{RESET_COLOR}'
        return message


class TimeColorFormatter(BaseColorFormatter):
    name = 'TimeColorFormatter'

    @staticmethod
    def _default_color() -> Dict[int, str]:
        return {
            # Notset: just black
            0: '',
            # Trace: blue
            2: '\033[0;34m',
            # Fine: green
            5: '\033[0;32m',
            # Debug: cyan
            7: '\033[0;36m',
            # Info: white
            10: '\033[0;37m',
            # Warn: yellow
            30: '\033[0;33m',
            # Error: red
            50: '\033[0;31m',
            # Fatal: red background
            90: '\033[0;41m',
        }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('colored time', 'time', 'A colored time')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[1].get('log_time') is None:
            return message
        # 向上寻找等级
        level = self.get_level(message, self._default_color())
        # 获取颜色
        color = self._default_color()[level]
        # 添加颜色
        message[1]['log_time'] = f'{color}{message[1]["log_time"]}{RESET_COLOR}'
        return message
