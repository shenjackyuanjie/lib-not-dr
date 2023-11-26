#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import List, Set, Dict

from lib_not_dr.logger.logger import Logger
from lib_not_dr.types.options import Options, OptionNameNotDefined
from lib_not_dr.logger.formatter import (MainFormatter,
                                         StdFormatter,
                                         BaseFormatter)
from lib_not_dr.logger.outstream import (BaseOutputStream,
                                         StdioOutputStream,
                                         FileCacheOutputStream)
from lib_not_dr.logger import formatter, outstream


class ConfigStorage(Options):
    name = 'LoggerConfigStorage'

    # 存储 logger, formatter, output 的字典
    loggers: Dict[str, Logger] = {}
    formatters: Dict[str, BaseFormatter] = {}
    outputs: Dict[str, BaseOutputStream] = {}
    # 存储失败的 logger, formatter, output 的字典
    fail_loggers: Dict[str, dict] = {}
    fail_formatters: Dict[str, dict] = {}
    fail_outputs: Dict[str, dict] = {}

    default_logger: Logger = Logger.get_logger_by_name('root')
    log: Logger = Logger.get_logger_by_name('logger-storage')

    def have_formatter(self, formatter_name: str) -> bool:
        return formatter_name in self.formatters

    def have_output(self, output_name: str) -> bool:
        return output_name in self.outputs

    def have_logger(self, logger_name: str) -> bool:
        return logger_name in self.loggers

    def merge_storage(self, other_storage: 'ConfigStorage') -> None:
        """
        Merge storage
        :param other_storage:
        :return:
        """
        self.loggers.update(other_storage.loggers)
        self.formatters.update(other_storage.formatters)
        self.outputs.update(other_storage.outputs)
        self.fail_loggers.update(other_storage.fail_loggers)
        self.fail_formatters.update(other_storage.fail_formatters)
        self.fail_outputs.update(other_storage.fail_outputs)

    # by GitHub Copilot
    @classmethod
    def _detect_cycle(cls, graph: Dict[str, List[str]], start: str, visited: Set[str], path: List[str]) -> List[str]:
        visited.add(start)  # 将当前节点添加到已访问的节点集合中
        path.append(start)  # 将当前节点添加到当前路径中
        for neighbour in graph[start]:  # 遍历当前节点的所有邻居
            if neighbour in visited:  # 如果邻居节点已经被访问过，那么我们找到了一个循环
                return path + [neighbour]  # 返回包含循环的路径
            cycle_path = cls._detect_cycle(graph, neighbour, visited, path)  # 递归地在邻居节点上调用函数
            if cycle_path:  # 如果在邻居节点上找到了循环，那么返回包含循环的路径
                return cycle_path
        visited.remove(start)  # 从已访问的节点集合中移除当前节点
        path.remove(start)  # 从当前路径中移除当前节点
        return []  # 如果没有找到循环，那么返回一个空列表

    @classmethod
    def find_cycles(cls, graph: Dict[str, List[str]]) -> List[str]:
        cycles_set = set()  # 创建一个集合来存储所有的循环
        for node in graph:  # 遍历图中的所有节点
            cycle = cls._detect_cycle(graph, node, set(), [])  # 在每个节点上调用detect_cycle函数
            if cycle:  # 如果找到了循环，那么将循环添加到集合中
                cycles_set.update(cycle)
        return sorted(cycles_set)  # 返回排序后的循环列表

    def parse_formatter(self, formatter_config: Dict[str, str]) -> 'ConfigStorage':
        """
        Parse formatter config
        :param formatter_config:
        :return:
        """
        env = ConfigStorage()
        formatter_wait: Dict[str, dict] = formatter_config.get('Formatter', {})

        # Check circle require
        formatter_require = {}
        for key, value in formatter_wait.items():
            if 'sub_formatter' in value:
                formatter_require[key] = value['sub_formatter']
            else:
                formatter_require[key] = []
        cycles_require = self.find_cycles(formatter_require)
        if cycles_require:
            for formatter_name in cycles_require:
                self.log.error(f'Formatter {formatter_name} require circle, ignored')
                env.fail_formatters[formatter_name] = formatter_wait[formatter_name]
                formatter_wait.pop(formatter_name)
        # Parse formatter
        ensure = 1000
        while len(formatter_wait) > 0:
            for key, value in formatter_wait.items():
                key: str
                value: dict
                formatter_name = key
                # check class
                if 'class' not in value:
                    self.log.warn(f'Formatter {formatter_name} has no class, ignored')
                    env.fail_formatters[formatter_name] = value
                    continue
                formatter_class = value.pop('class')
                # check class exist
                if formatter_class not in formatter.__all__:
                    self.log.warn(f'Formatter {formatter_name} class {formatter_class} not found, ignored')
                    env.fail_formatters[formatter_name] = value
                    continue
                formatter_class = getattr(formatter, formatter_class)
                # ensure sub formatter exist
                if 'sub_formatter' in value:
                    for fmt in value['sub_formatter']:
                        if not env.have_formatter(fmt):
                            formatter_wait[formatter_name] = value
                            continue
                # init formatter
                try:
                    formatter_instance = formatter_class(**value)
                except OptionNameNotDefined as e:
                    self.log.error(f'Formatter {formatter_name} class {formatter_class} init failed, ignored\n'
                                   f'Error: {e}')
                    env.fail_formatters[formatter_name] = value
                    continue
                # add formatter
                env.formatters[formatter_name] = formatter_instance
                formatter_wait.pop(formatter_name)
            ensure -= 1
            if ensure <= 0:
                self.log.error('Formatter parse failed, ignored')
                # add all left formatter to fail formatter
                env.fail_formatters.update(formatter_wait)
                break
        return env

    def read_dict_config(self, config: Dict[str, dict]) -> None:
        """
        Read config from dict
        :param config:
        :return:
        """
        dict_env = self.parse_formatter(config.get('Formatter', {}))

        self.merge_storage(dict_env)


storage = ConfigStorage()
