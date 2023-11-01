#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import inspect
import unittest

from lib_not_dr.logger.formatter import BaseFormatter, TimeFormatter, LevelFormatter, TraceFormatter
from lib_not_dr.logger.structers import LogMessage


class FormatterTest(unittest.TestCase):

    def test_create_message(self):
        message = LogMessage(messages=['test'],
                             level=20,
                             logger_name='root',
                             logger_tag='root',
                             stack_trace=inspect.currentframe())
        self.assertEqual(message.messages, ['test'])
        self.assertEqual(message.level, 20)
        self.assertEqual(message.logger_name, 'root')
        self.assertEqual(message.logger_tag, 'root')

    def test_create_empty_tag_message(self):
        message = LogMessage()

        self.assertIsNone(message.logger_tag)
        self.assertEqual(message.format_for_message()['logger_tag'], '   ')

    def test_formatter(self):
        formatter = BaseFormatter()
        formatter.info()

    def test_time_formatter(self):
        formatter = TimeFormatter()
        formatter.info()

    def test_level_formatter(self):
        formatter = LevelFormatter()
        formatter.info()

    def test_std_formatter(self):
        formatter = BaseFormatter()
        formatter.info()

    def test_trace_formatter(self):
        formatter = TraceFormatter()
        formatter.info()
