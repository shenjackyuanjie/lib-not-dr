#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import unittest

from lib_not_dr.command.nodes import Literal


class CommandBuildTest(unittest.TestCase):
    """ 仅测试命令的构建 """

    def test_basic_command(self):  # NOQA
        Literal("test")

    def test_sub_command(self):  # NOQA
        Literal("test")(
            Literal("more"),
            Literal("and"),
            Literal("lot_more")
        )

    def test_command_str_tip(self):
        command = Literal("test").tip('tip for test')
        self.assertEqual(command._tip, 'tip for test')

    def test_command_callable_tip(self):
        def tip():
            return 'tip for test'

        command = Literal("test").tip(tip)
        self.assertEqual(command._tip, tip)

    def test_command_arg(self):  # NOQA
        Literal("test").arg("arg1", {int, }, "tip for arg1")

    def test_command_flag(self):  # NOQA
        Literal("test").flag("flag1", None, "tip for flag1")

    def test_command_run(self):
        def run():
            print("test run")

        command = Literal("test").run(run)
        self.assertEqual(command._func, run)


class CommandParseTest(unittest.TestCase):
    """ 测试命令的解析 """

    def test_basic_command(self):
        command = Literal("test").tip("tip for test")
        self.assertEqual("tip for test", command.parse("test"))
        # 无 error/run 默认返回 tip

    def test_sub_command(self):
        command = Literal("test")\
            .tip("tip for test")(
            Literal("more")
            .tip("tip for more"),
            Literal("more2")
            .tip("tip for more2"),
        )
        self.assertEqual("tip for test", command.parse("test"))
        self.assertEqual("tip for more", command.parse("test more"))
        self.assertEqual("tip for more2", command.parse("test more2"))


if __name__ == '__main__':
    unittest.main()
