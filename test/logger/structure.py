#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import unittest

from lib_not_dr.logger.structure import LogMessage


class LogMessageTest(unittest.TestCase):
    def test_create_empty_message(self):
        """
        测试空消息的创建
        这玩意甚至是 codeiume/github copilot 自动补全的
        """
        message = LogMessage()
        self.assertEqual(message.messages, [])
        self.assertEqual(message.level, 20)
        self.assertEqual(message.logger_name, 'root')
        self.assertEqual(message.logger_tag, None)

    def test_format_message_empty(self):
        """
        测试空消息的格式化
        因为才发现空信息之前的格式化是有问题的(因为没有初始化 messages)
        """
        message = LogMessage()
        self.assertEqual(message.format_message(), '\n')

    def test_format_message_end(self):
        """
        测试消息的结尾
        """
        message = LogMessage(messages=['test'],
                             end='\n')
        for testing in ('\n', '\r\n', '\r'):
            message.end = testing
            self.assertEqual(message.format_message(), 'test' + testing)

    def test_format_message_split(self):
        """
        测试消息的分割
        """
        message = LogMessage(messages=['test', 'test2'], end='')
        for testing in (' ', ' | ', ' | '):
            message.split = testing
            self.assertEqual(message.format_message(), 'test' + testing + 'test2')

    def test_format_message_end_with_split(self):
        """
        测试消息的结尾和分割
        """
        message = LogMessage(messages=['test', 'test2'], end='\n')
        for test_split in (' ', ' | ', ' | '):
            for test_end in ('\n', '\r\n', '\r'):
                message.split = test_split
                message.end = test_end
                self.assertEqual(message.format_message(), 'test' + test_split + 'test2' + test_end)

    def test_msec_3(self):
        start_time = time.time()
        message = LogMessage(log_time=start_time)
        msec_3 = int(start_time / 1000000) % 1000
        self.assertEqual(message.create_msec_3, msec_3)
