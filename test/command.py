#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import unittest

from lib_not_dr.command.nodes import Literal


class CommandTest(unittest.TestCase):

    def test_basic_command(self):
        Literal("test")
