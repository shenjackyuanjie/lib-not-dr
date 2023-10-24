#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time

from string import Template
from typing import List, Union, Optional
from lib_not_dr.types.options import Options

from structers import LogMessage, FormattingMessage


class BaseFormatter(Options):
    name = 'BaseFormatter'

    sub_formatter: List['BaseFormatter'] = []
    default_template: str = '${log_time}|${logger_name}|${logger_tag}|${level}|${messages}'

    @classmethod
    def add_info(cls, match: str, to: str, description: str) -> str:
        return f'- {to} -> ${{{match}}} : {description}'

    @classmethod
    def info(cls) -> str:
        cache = "## Base Formatter\n"
        cache += BaseFormatter._info()
        cache += f"## {cls.name}\n"
        cache += cls._info()
        for formatter in cls.sub_formatter:
            cache += formatter.info()
        return cache

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('logger_name', 'logger name', 'The name of the logger')
        info += '\n'
        info += cls.add_info('logger_tag', 'logger tag', 'The tag of the logger')
        info += '\n'
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
        0: 'NOTSET',
        10: 'TRACE',
        20: 'FINE',
        30: 'DEBUG',
        40: 'INFO',
        50: 'WARN',
        60: 'ERROR',
        70: 'FATAL'
    }
    name_level_map = {
        'NOTSET': 0,
        'TRACE': 10,
        'FINE': 20,
        'DEBUG': 30,
        'INFO': 40,
        'WARN': 50,
        'ERROR': 60,
        'FATAL': 70
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


if __name__ == '__main__':
    print(TimeFormatter.info())
    print(TimeFormatter().format_message(LogMessage(messages=['Hello World!'])))

    print(LevelFormatter.info())
    print(LevelFormatter().format_message(LogMessage(messages=['Hello World!'], level=10)))
