#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import inspect

from lib_not_dr.logger.structers import LogMessage
from lib_not_dr.logger.formatter import (StdFormatter,
                                         TimeFormatter,
                                         LevelFormatter,
                                         TraceFormatter)


if __name__ == '__main__':

    levels = (0, 2, 5, 7, 10, 30, 50, 90)

    log_message = LogMessage(messages=['Hello World!'],
                             level=7,
                             stack_trace=inspect.currentframe(),
                             logger_tag='tester',
                             logger_name='test')

    print(StdFormatter.info())
    print(StdFormatter().format_message(log_message))

    std_format = StdFormatter()
    std_format.default_template = "${log_time}|${logger_name}|${logger_tag}|${log_source}:${log_line}|${log_function}|${level}|${messages}"

    test_levels = (0, 2, 5, 7, 10, 30, 50, 90)

    print("with color")

    for test_level in test_levels:
        log_message.level = test_level
        print(std_format.format_message(log_message), end='')

    print(std_format.as_markdown())

    print("without color")

    std_format.enable_color = False

    for test_level in test_levels:
        log_message.level = test_level
        print(std_format.format_message(log_message), end='')

    print(std_format.as_markdown())