#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Dict, Tuple

from lib_not_dr.logger.formatter import BaseFormatter
from lib_not_dr.logger.structure import FormattingMessage


__all__ = [
    'BaseColorFormatter',

    'LevelColorFormatter',
    'LoggerColorFormatter',
    'TimeColorFormatter',
    'TraceColorFormatter',
    'MessageColorFormatter',

    'RESET_COLOR'
]

RESET_COLOR = '\033[0m'


class BaseColorFormatter(BaseFormatter):
    name = 'BaseColorFormatter'
    # TODO 迁移老 logger 颜色
    color = {
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

    def get_color(self, message: FormattingMessage) -> str:
        for level in self.color:
            if message[0].level <= level:
                break
        else:
            level = 90
        return self.color[level]


class LevelColorFormatter(BaseColorFormatter):
    name = 'LevelColorFormatter'
    # TODO 迁移老 logger 颜色
    color = {
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
        # 获取颜色
        color = self.get_color(message)
        # 添加颜色
        if color == '' or color == RESET_COLOR:
            return message
        message[1]['level'] = f'{color}{message[1]["level"]}{RESET_COLOR}'
        return message


class LoggerColorFormatter(BaseColorFormatter):
    name = 'LoggerColorFormatter'
    # TODO 迁移老 logger 颜色
    color = {
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
        90: '\033[38;2;245;189;230m',
    }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('colored logger name', 'logger name', 'A colored logger name')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[1].get('logger_name') is None:
            return message
        # 获取颜色
        color = self.get_color(message)
        # 添加颜色
        if color == '' or color == RESET_COLOR:
            return message
        message[1]['logger_name'] = f'{color}{message[1]["logger_name"]}{RESET_COLOR}'
        if message[1].get('logger_tag') is not None and message[1].get('logger_tag') != '   ':
            message[1]['logger_tag'] = f'{color}{message[1]["logger_tag"]}{RESET_COLOR}'
        return message


class TimeColorFormatter(BaseColorFormatter):
    name = 'TimeColorFormatter'
    # TODO 迁移老 logger 颜色
    color = {
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
        # 获取颜色
        color = self.get_color(message)
        # 添加颜色
        if color == '' or color == RESET_COLOR:
            return message
        message[1]['log_time'] = f'{color}{message[1]["log_time"]}{RESET_COLOR}'
        return message


class TraceColorFormatter(BaseColorFormatter):
    name = 'TraceColorFormatter'
    # TODO 迁移老 logger 颜色
    color = {
        # Notset: just black
        0: '\033[38;2;0;255;180m',
        # Trace: blue
        2: '\033[38;2;0;255;180m',
        # Fine: green
        5: '\033[38;2;0;255;180m',
        # Debug: cyan
        7: '\033[38;2;0;255;180m',
        # Info: white
        10: '\033[38;2;0;255;180m',
        # Warn: yellow
        30: '\033[38;2;0;255;180m',
        # Error: red
        50: '\033[38;2;0;255;180m',
        # Fatal: red background
        90: '\033[38;2;0;255;180m',
    }

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('colored logging file', 'log_source', 'A colored logging file name')
        info += '\n'
        info += cls.add_info('colored logging line', 'log_line', 'A colored logging line number')
        info += '\n'
        info += cls.add_info('colored logging function', 'log_function', 'A colored logging function name')
        return info

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[0].stack_trace is None:
            return message
        # 获取颜色
        color = self.get_color(message)
        # 添加颜色
        if color == '' or color == RESET_COLOR:
            return message
        message[1]['log_source'] = f'{color}{message[1]["log_source"]}{RESET_COLOR}'
        message[1]['log_line'] = f'{color}{message[1]["log_line"]}{RESET_COLOR}'
        message[1]['log_function'] = f'{color}{message[1]["log_function"]}{RESET_COLOR}'
        return message


class MessageColorFormatter(BaseColorFormatter):
    name = 'MessageColorFormatter'

    color = {
        # Notset: just black
        0: '',
        # Trace: blue
        2: '\033[38;2;138;173;244m',
        # Fine: blue
        5: '\033[38;2;138;173;244m',
        # Debug: blue
        7: '\033[38;2;138;173;244m',
        # Info: no color
        10: '',
        # Warn: yellow
        30: '\033[0;33m',
        # Error: red
        50: '\033[0;31m',
        # Fatal: red background
        90: '\033[38;2;255;255;0;48;2;120;10;10m',
    }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('colored message', 'message', 'A colored message')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[1].get('messages') is None:
            return message
        # 获取颜色
        color = self.get_color(message)
        # 添加颜色
        if color == '' or color == RESET_COLOR:
            return message
        if message[1]['messages'][-1] == '\n':
            message[1]['messages'] = f'{color}{message[1]["messages"][:-1]}{RESET_COLOR}\n'
        else:
            message[1]['messages'] = f'{color}{message[1]["messages"]}{RESET_COLOR}'
        return message
