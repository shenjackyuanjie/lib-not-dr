#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import time

from string import Template
from typing import List, Union, Optional, Dict, Tuple

from lib_not_dr.types.options import Options
from lib_not_dr.logger.structers import LogMessage, FormattingMessage


class BaseFormatter(Options):
    name = 'BaseFormatter'

    sub_formatter: List['BaseFormatter'] = []
    default_template: str = '${log_time}|${logger_name}|${logger_tag}|${level}|${messages}'

    @classmethod
    def add_info(cls, match: str, to: str, description: str) -> str:
        return f'- {to} -> ${{{match}}} : {description}'

    @classmethod
    def info(cls) -> str:
        infos = {BaseFormatter.name: BaseFormatter._info()}
        cache = ''
        for formatter in cls.sub_formatter:
            infos[formatter.name] = formatter._info()
        infos[cls.name] = cls._info()
        for name, info in infos.items():
            cache += f"## {name}\n"
            cache += info
            cache += '\n'
        return cache

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('logger_name', 'logger name', 'The name of the logger')
        info += '\n'
        info += cls.add_info('logger_tag', 'logger tag', 'The tag of the logger')
        return info

    def format_message(self,
                       message: LogMessage,
                       template: Optional[Union[Template, str]] = None) -> str:
        """
        Format message
        :param message: 输入的消息
        :param template: 日志输出模板
        :return:
        """
        basic_info = message.format_for_message()
        message, info = self._format((message, basic_info))

        if template is None:
            template = Template(self.default_template)
        elif isinstance(template, str):
            template = Template(template)

        try:
            return template.substitute(**info)
        except (KeyError, ValueError):
            return template.safe_substitute(**info)

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        """
        Format message
        :param message:
        :return:
        """
        for formatter in self.sub_formatter:
            message = formatter._format(message)
        return message


class TimeFormatter(BaseFormatter):
    name = 'TimeFormatter'

    time_format: str = '%Y-%m-%d %H:%M:%S'
    msec_time_format: str = '{}-{:03d}'

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('log_time', 'formatted time when logging', 'The time format string'
                                                                       '. See https://docs.python.org/3/library/time.html#time.strftime for more information.')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        time_mark = time.localtime(message[0].log_time / 1000000000)
        if self.msec_time_format:
            time_mark = self.msec_time_format.format(time.strftime(self.time_format, time_mark),
                                                     message[0].create_msec_3)
        message[1]['log_time'] = time_mark
        return message


class LevelFormatter(BaseFormatter):
    name = 'LevelFormatter'

    default_level: int = 20

    # If True, the undefined level will be set to the higher nearest level.
    level_get_higher: bool = True

    level_name_map = {
        0:  'NOTSET',
        2:  'TRACE',
        5:  'FINE',
        7:  'DEBUG',
        10: 'INFO',
        30: 'WARN',
        50: 'ERROR',
        90: 'FATAL'
    }
    name_level_map = {
        'NOTSET': 0,
        'TRACE':  2,
        'FINE':   5,
        'DEBUG':  7,
        'INFO':   10,
        'WARN':   30,
        'ERROR':  50,
        'FATAL':  90
    }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('level', 'log level', 'The log level')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[0].level in self.name_level_map:
            level_tag = self.level_name_map[message[0].level]
        else:
            if self.level_get_higher:
                for level in self.name_level_map:
                    if message[0].level < self.name_level_map[level]:
                        level_tag = level
                        break
                else:
                    level_tag = 'FATAL'
            else:
                for level in self.name_level_map:
                    if message[0].level > self.name_level_map[level]:
                        level_tag = level
                        break
                else:
                    level_tag = 'NOTSET'
        message[1]['level'] = level_tag
        return message


class TraceFormatter(BaseFormatter):
    name = 'TraceFormatter'

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('logging file', 'log_source', 'the logging file name')
        info += '\n'
        info += cls.add_info('logging line', 'log_line', 'the logging line number')
        info += '\n'
        info += cls.add_info('logging function', 'log_function', 'the logging function name')
        return info

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[0].stack_trace is None:
            return message
        message[1]['log_source'] = message[0].stack_trace.f_code.co_filename
        message[1]['log_line'] = message[0].stack_trace.f_lineno
        message[1]['log_function'] = message[0].stack_trace.f_code.co_name
        return message


class LevelColorFormatter(BaseFormatter):
    name = 'LevelColorFormatter'

    enable_color: bool = True

    @staticmethod
    def _default_color() -> Dict[int, Tuple[str, str]]:
        return {
            # Notset: just black
            0: ('', ''),
            # Trace: blue
            2: ('\033[0;34m', '\033[0m'),
            # Fine: green
            5: ('\033[0;32m', '\033[0m'),
            # Debug: cyan
            7: ('\033[0;36m', '\033[0m'),
            # Info: white
            10: ('\033[0;37m', '\033[0m'),
            # Warn: yellow
            30: ('\033[0;33m', '\033[0m'),
            # Error: red
            50: ('\033[0;31m', '\033[0m'),
            # Fatal: red
            90: ('\033[0;31m', '\033[0m')
        }

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('colored message', 'message', 'A colored message')
        info += '\n'
        info += cls.add_info('colored level', 'level', 'A colored level')
        info += '\n'
        info += cls.add_info('colored logger name', 'logger_name', 'A colored logger name')
        return info

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[1].get('level') is None:
            return message
        # 向上寻找等级
        for level in self._default_color():
            if message[0].level < level:
                break
        else:
            level = 90
        # 获取颜色
        color = self._default_color()[level]
        # 添加颜色
        message[1]['messages'] = f'{color[0]}{message[1]["messages"]}{color[1]}'
        message[1]['level'] = f'{color[0]}{message[1]["level"]}{color[1]}'
        message[1]['logger_name'] = f'{color[0]}{message[1]["logger_name"]}{color[1]}'
        return message


class StdFormatter(BaseFormatter):
    name = 'StdFormatter'

    sub_formatter = [TimeFormatter(), LevelFormatter(), TraceFormatter(), LevelColorFormatter()]

    @classmethod
    def _info(cls) -> str:
        return 'None'


if __name__ == '__main__':
    import inspect

    log_message = LogMessage(messages=['Hello World!'],
                             level=10,
                             stack_trace=inspect.currentframe(),
                             logger_tag='tester',
                             logger_name='test')

    print(TimeFormatter.info())
    print(TimeFormatter().format_message(log_message))

    print(LevelFormatter.info())
    print(LevelFormatter().format_message(log_message))

    print(TraceFormatter.info())
    print(TraceFormatter().format_message(log_message))

    print(LevelColorFormatter.info())
    print(LevelColorFormatter().format_message(log_message))

    print(StdFormatter.info())
    print(StdFormatter().format_message(log_message))
