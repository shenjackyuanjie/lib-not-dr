#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import List, Set, Dict, Optional, Tuple

from lib_not_dr.loggers.logger import Logger
from lib_not_dr.loggers.formatter import BaseFormatter
from lib_not_dr.loggers.outstream import BaseOutputStream
from lib_not_dr.loggers import formatter, outstream, LogLevel
from lib_not_dr.types.options import Options, OptionNameNotDefined


class ConfigStorage(Options):
    name = "LoggerConfigStorage"

    # 存储 logger, formatter, output 的字典
    loggers: Dict[str, Logger] = {}
    formatters: Dict[str, BaseFormatter] = {}
    outputs: Dict[str, BaseOutputStream] = {}
    # 存储失败的 logger, formatter, output 的字典
    fail_loggers: Dict[str, dict] = {}
    fail_formatters: Dict[str, dict] = {}
    fail_outputs: Dict[str, dict] = {}

    log: Logger = Logger(logger_name="loggers-storage")

    def have_formatter(self, formatter_name: str) -> bool:
        return formatter_name in self.formatters

    def have_output(self, output_name: str) -> bool:
        return output_name in self.outputs

    def have_logger(self, logger_name: str) -> bool:
        return logger_name in self.loggers

    def merge_storage(self, other_storage: "ConfigStorage") -> None:
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
    def _detect_cycle(
        cls,
        graph: Dict[str, List[str]],
        start: str,
        visited: Set[str],
        path: List[str],
    ) -> List[str]:
        visited.add(start)  # 将当前节点添加到已访问的节点集合中
        path.append(start)  # 将当前节点添加到当前路径中
        for neighbour in graph[start]:  # 遍历当前节点的所有邻居
            if (
                neighbour in visited
            ):  # 如果邻居节点已经被访问过，那么我们找到了一个循环
                return path + [neighbour]  # 返回包含循环的路径
            cycle_path = cls._detect_cycle(
                graph, neighbour, visited, path
            )  # 递归地在邻居节点上调用函数
            if cycle_path:  # 如果在邻居节点上找到了循环，那么返回包含循环的路径
                return cycle_path
        visited.remove(start)  # 从已访问的节点集合中移除当前节点
        path.remove(start)  # 从当前路径中移除当前节点
        return []  # 如果没有找到循环，那么返回一个空列表

    @classmethod
    def find_cycles(cls, graph: Dict[str, List[str]]) -> List[str]:
        cycles_set = set()  # 创建一个集合来存储所有的循环
        for node in graph:  # 遍历图中的所有节点
            cycle = cls._detect_cycle(
                graph, node, set(), []
            )  # 在每个节点上调用detect_cycle函数
            if cycle:  # 如果找到了循环，那么将循环添加到集合中
                cycles_set.update(cycle)
        return sorted(cycles_set)  # 返回排序后的循环列表

    def parse_level(self, level_config: dict) -> Optional[int]:
        """ """
        level_found: Tuple[Optional[int], Optional[str]] = (
            level_config.get("level"),
            level_config.get("level_name"),
        )
        if all(_l is None for _l in level_found):
            # 如果都没有
            self.log.warn(
                f"No level or level_name in config {level_config}, ignored"
            )
            return 20
        if all(_l is not None for _l in level_found):
            # 如果都有 那么使用 level_name
            self.log.warn(
                f"Level and level_name both exist in config {level_config}, using level_name"
            )
            # 去掉 level 保留 level_name
            level_found = (
                None,
                level_found[1],
            )
        if level_found[0] is not None:
            # 如果 level 存在 那么使用 level
            return level_found[0]
        if level_found[1] is not None:
            # 如果 level_name 存在 那么使用 level_name
            return LogLevel.parse_name_level(level_found[1])
        return None

    def get_class_by_name(
        self, config: Dict[str, str], module
    ) -> Optional[type]:
        """
        Get class by name
        :param config:
        :param module:
        :return:
        """
        # check class
        if "class" not in config:
            self.log.warn(f"No class in config {config}, ignored")
            return None
        class_name = config.pop("class")
        # check class exist
        if class_name not in module.__all__:
            self.log.warn(
                f"Class {class_name} not found in module {module}, ignored"
            )
            return None

        return getattr(module, class_name)

    def parse_formatter(self, formatter_config: Dict[str, dict]) -> None:
        """
        Parse formatter config
        :param formatter_config:
        :return:
        """
        env = ConfigStorage()

        # Check circle require
        formatter_require = {}
        for key, value in formatter_config.items():
            if "sub_formatter" in value:
                formatter_require[key] = value["sub_formatter"]
            else:
                formatter_require[key] = []
        cycles_require = self.find_cycles(formatter_require)
        # 去除循环依赖
        if cycles_require:
            for formatter_name in cycles_require:
                self.log.error(
                    f"Formatter {formatter_name} have a cycle require, ignored"
                )
                env.fail_formatters[formatter_name] = formatter_config[
                    formatter_name
                ]
                formatter_config.pop(formatter_name)
        # Parse formatter
        ensure = 1000
        while len(formatter_config) > 0:
            pop_list = []
            for key, value in formatter_config.items():
                key: str
                value: dict
                formatter_name = key
                # check class
                formatter_class = self.get_class_by_name(value, formatter)
                if formatter_class is None:
                    env.fail_formatters[formatter_name] = value
                    pop_list.append(key)
                    continue
                # ensure sub formatter exist
                if "sub_formatter" in value:
                    fmts = []
                    for fmt in value["sub_formatter"]:
                        if not env.have_formatter(fmt):
                            formatter_config[formatter_name] = value
                            continue
                        fmts.append(env.formatters[fmt])
                    value["sub_formatter"] = fmts
                # init formatter
                try:
                    formatter_instance = formatter_class(**value)
                except OptionNameNotDefined as e:
                    self.log.error(
                        f"Formatter {formatter_name} class {formatter_class} init failed, ignored\n"
                        f"Error: {e}"
                    )
                    env.fail_formatters[formatter_name] = value
                    pop_list.append(key)
                    continue
                # add formatter
                env.formatters[formatter_name] = formatter_instance
                pop_list.append(key)
            # pop formatter
            for key in pop_list:
                formatter_config.pop(key)

            ensure -= 1
            if ensure <= 0:
                self.log.error(
                    "Formatter parse failed, ignored\n"
                    f"Left formatters: {formatter_config}"
                )
                # add all left formatter to fail formatter
                env.fail_formatters.update(formatter_config)
                break
        self.merge_storage(env)
        return None

    def parse_output(self, output_config: Dict[str, dict]) -> None:
        """
        Parse output config
        :param output_config:
        :return:
        """
        env = ConfigStorage()
        for output_name, config in output_config.items():
            # check class
            output_class = self.get_class_by_name(config, outstream)
            if output_class is None:
                env.fail_outputs[output_name] = config
                continue
            # get formatter for output
            if "formatter" in config:
                if self.formatters.get(config["formatter"]) is None:
                    if self.fail_formatters.get(config["formatter"]) is None:
                        self.log.error(
                            f'Output {output_name} formatter {config["formatter"]} not found, ignored'
                        )
                    else:
                        self.log.error(
                            f'Output {output_name} require a fail formatter {config["formatter"]}, ignored'
                        )
                    env.fail_outputs[output_name] = config
                    continue
                else:
                    config["formatter"] = self.formatters[config["formatter"]]
            if level := self.parse_level(config) is not None:
                config["level"] = level
            if "level_name" in config:
                config.pop("level_name")
            # init output
            try:
                output_instance = output_class(**config)
            except OptionNameNotDefined as e:
                self.log.error(
                    f"Output {output_name} class {output_class} init failed, ignored\n"
                    f"Error: {e}"
                )
                env.fail_outputs[output_name] = config
                continue
            # add output
            env.outputs[output_name] = output_instance
        self.merge_storage(env)
        return None

    def parse_logger(self, logger_config: Dict[str, dict]) -> None:
        """
        Parse loggers config
        :param logger_config: config of loggers
        """
        env = ConfigStorage()
        for logger_name, config in logger_config.items():
            # get output for logger
            if "outputs" in config:
                if self.outputs.get(config["outputs"]) is None:
                    if self.fail_outputs.get(config["outputs"]) is None:
                        self.log.error(
                            f'Logger {logger_name} output {config["output"]} not found, ignored'
                        )
                    else:
                        self.log.error(
                            f'Logger {logger_name} require a fail output {config["output"]}, ignored'
                        )
                    env.fail_loggers[logger_name] = config
                    continue
                else:
                    config["outputs"] = self.outputs[config["outputs"]]
            if level := self.parse_level(config) is not None:
                config["level"] = level
            if "level_name" in config:
                config.pop("level_name")
            # init logger
            try:
                logger_instance = Logger(**config)
            except OptionNameNotDefined as e:
                self.log.error(
                    f"Logger {logger_name} init failed, ignored\n" f"Error: {e}"
                )
                env.fail_loggers[logger_name] = config
                continue
            # add logger
            env.loggers[logger_name] = logger_instance
        self.merge_storage(env)
        return None

    def read_dict_config(self, config: Dict[str, dict]) -> None:
        """
        Read config from dict
        :param config:
        :return:
        """
        self.parse_formatter(config.get("Formatter", {}))
        self.parse_output(config.get("Outstream", {}))
        self.parse_logger(config.get("Logger", {}))


_storage = ConfigStorage(loggers={'root': Logger(logger_name='root')})


def get_config() -> ConfigStorage:
    return _storage


def get_logger(name: str = 'root', storage: Optional[ConfigStorage] = None) -> Logger:
    if storage is None:
        storage = _storage

    if name not in storage.loggers:
        root_log = storage.loggers['root'].clone_logger()
        root_log.logger_name = name
        storage.loggers[name] = root_log
    return storage.loggers[name]


def read_config(log_config: Dict, storage: Optional[ConfigStorage] = None) -> ConfigStorage:
    if storage is None:
        storage = _storage

    storage.read_dict_config(log_config)
    return storage
