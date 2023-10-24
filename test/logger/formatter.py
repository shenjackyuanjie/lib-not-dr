#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import unittest

from lib_not_dr.logger.formatter import BaseFormatter, TimeFormatter, LevelFormatter
from lib_not_dr.logger.structers import LogMessage


class FormatterTest(unittest.TestCase):

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
