#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import re
from dataclasses import dataclass
from typing import Callable, List, Optional, Union

from .descriptor import CallBackDescriptor

try:
    from typing import Self
except ImportError:
    from typing import TypeVar
    Self = TypeVar("Self")

from .exception import IllegalArgumentName

CallBack = Union[Callable[[str], None], str]  # Equals to `Callable[[str], None] | str`
# 可调用对象或字符串作为回调
# A callable or str as callback

ParseArgFunc = Callable[[str], Optional[type]]
# 解析参数的函数，返回值为 None 时表示解析失败
# function to parse argument, return None when failed

EMPTY_WORDS = re.compile(r"\s", re.I)


def check_once(cls, name) -> None:
    """
    Check whether the attribute has been set.
    if so, it will raise exception `AttributeError`.
    检查属性是否已经被设置。
    如果已经被设置，将会抛出 `AttributeError` 异常。
    :param cls: class object
    :param name: attribute name
    :return: None
    """
    if hasattr(cls, name):
        if getattr(cls, name) is not None:
            raise AttributeError(f"Attribute '{name}' has been set.")


def check_name(name: Union[str, List[str]]) -> None:
    """
    Check the name or shortcuts of argument(s) or flag(s).
    The name must not be empty str, and must not contains \\t or \\n or \\f or \\r.
    If that not satisfy the requirements, it will raise exception `IllegalArgumentName`.
    检查 参数或标记 的 名称或快捷方式 是否符合要求。
    名称必须是非空的字符串，且不能包含 \\t 或 \\n 或 \\f 或 \\r。
    如果不符合要求，将会抛出 `IllegalArgumentName` 异常。
    :param name: arguments
    :return: None
    """
    if isinstance(name, str) and EMPTY_WORDS.search(name):
        raise IllegalArgumentName("The name of argument must not contains empty words.")
    elif isinstance(name, list) and all((not isinstance(i, str)) and EMPTY_WORDS.search(i) for i in name):
        raise IllegalArgumentName("The name of shortcut must be 'str', and must not contains empty words.")
    else:
        raise TypeError("The type of name must be 'str' or 'list[str]'.")


class Parsed:
    ...


@dataclass
class Argument:
    name: str
    shortcuts: List[str]
    optional: bool
    type: type


@dataclass
class Flag:
    name: str
    shortcuts: List[str]


class Literal:
    _tip = CallBackDescriptor("_tip")
    _func = CallBackDescriptor("_func")
    _err_callback = CallBackDescriptor("_err_callback")

    def __init__(self, name: str):
        self.name: str = name
        self.sub: List[Self] = []

        self._doc: Optional[str] = None
        self._tip: Optional[CallBack] = None
        self._func: Optional[CallBack] = None
        self._err_callback: Optional[CallBack] = None
        self._args: List[Argument] = []
        self._flags: List[Argument]

    def __call__(self, *nodes) -> Self:
        self.sub += nodes
        return self

    def __repr__(self):
        attrs = (k for k in self.__dict__ if not (k.startswith("__") and k.endswith("__")))
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k in attrs if (v := self.__dict__[k]))})"

    def arg(
            self,
            name: str,
            shortcuts: Optional[List[str]] = None,
            optional: bool = True,
            type: Optional[type] = None
    ) -> Self:
        check_name(name)
        if shortcuts is not None and len(shortcuts) != 0:
            check_name(shortcuts)
        Argument(name=name, shortcuts=shortcuts, optional=optional, type=type)
        return self

    def arg_group(self, args: List[Argument], exclusive: bool = False):
        ...

    def flag(self, name: str, shortcuts: Optional[List[str]] = None) -> Self:
        check_name(name)
        if shortcuts is not None and len(shortcuts) != 0:
            check_name(shortcuts)
        # Flag(...)
        ...
        return self

    def flag_group(self, flags: List[Flag], exclusive: bool = False):
        ...

    def error(self, callback: CallBack) -> Self:
        self._err_callback = callback
        return self

    def run(self, func: CallBack) -> Self:
        self._func = func
        return self

    def tip(self, tip: CallBack) -> Self:
        self._tip = tip
        return self

    def parse(self, cmd: Union[str, List[str]]) -> Parsed:
        ...

    def to_doc(self) -> str:
        ...
        self._doc = ...
        return self._doc


def builder(node: Literal) -> Literal:
    ...
