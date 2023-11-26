#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import unittest

from lib_not_dr.logger.config import ConfigStorage


class TestConfigStorage(unittest.TestCase):
    def test_detect_circle_require(self):
        test_dict = {
            'a': ['b', 'c'],
            'b': ['c'],
            'c': ['a'],
            'd': ['e'],
            'e': ['f'],
            'f': ['d']
        }
        self.assertEqual(['a', 'b', 'c', 'd', 'e', 'f'], ConfigStorage.find_cycles(test_dict))

    def test_detect_circle_require_2(self):
        # large circle
        cycles = sorted(map(str, range(100)))
        for i in range(100):
            test_dict = {}
            for j in range(100):
                test_dict[str(j)] = [str((j + 1) % 100)]
            self.assertEqual(cycles, ConfigStorage.find_cycles(test_dict))

    def test_detect_circle_require_3(self):
        # normal
        test_dict = {'a': [], 'b': ['a'], 'c': ['b'], 'd': ['c']}
        self.assertEqual([], ConfigStorage.find_cycles(test_dict))

    def test_parse_formatter_config(self):
        test_config = {
            'main': {
                'class': 'MainFormatter',
                'sub_formatter': []
            },
            'cycle_a': {
                'class': 'MainFormatter',
                'sub_formatter': ['cycle_b']
            },
            'cycle_b': {
                'class': 'MainFormatter',
                'sub_formatter': ['cycle_a']
            }
        }
        test_storage = ConfigStorage()
        test_storage.parse_formatter(test_config)
        self.assertTrue(test_storage.have_formatter('main'))
        self.assertFalse(test_storage.have_formatter('cycle_a'))
        self.assertFalse(test_storage.have_formatter('cycle_b'))
