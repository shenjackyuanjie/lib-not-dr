#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  and MSDNicrosoft
#  All rights reserved
#  -------------------------------

from typing import List, Optional, Union, Set, Iterable

from .data import (
    CommandOption,
    CommandArgument,
    CommandFlag,
    Parsed,
    CommandOptionGroup,
    CommandFlagGroup,
    CallBack,
ParseArgFunc,
EMPTY_WORDS,
)
from .descriptor import CallBackDescriptor

try:
    from typing import Self
except ImportError:
    from typing import TypeVar

    Self = TypeVar("Self")  # NOQA

from .exception import IllegalName



def get_element(text: str) -> str:
    """
    Get the first element of text.
    :param text: text
    :return: the first element
    """
    pos = text.find(' ')
    if pos == -1:
        return text
    else:
        return text[:pos]


def check_name(name: Union[str, Iterable[str]]) -> None:
    """
    Check the name or shortcuts of argument(s) or flag(s).
    The name must not be empty str, and must not contain empty words.
    If that not satisfy the requirements, it will raise exception `IllegalArgumentName`.
    检查 参数或标记 的 名称或快捷方式 是否符合要求。
    名称必须是非空的字符串，且不能包含各种空格。
    如果不符合要求，将会抛出 `IllegalArgumentName` 异常。
    :param name: arguments
    :return: None
    """
    if isinstance(name, str):
        if EMPTY_WORDS.search(name) is not None:
            raise IllegalName("The name of argument must not contains empty words.")
    elif isinstance(name, Iterable):
        if any((not isinstance(i, str)) or EMPTY_WORDS.search(i) is not None for i in name):
            raise IllegalName("The name of shortcut must be 'str', and must not contains empty words.")
    else:
        raise TypeError("The type of name must be 'str' or 'Iterable[str]'.")


class Literal:
    _tip = CallBackDescriptor("_tip")
    _func = CallBackDescriptor("_func")
    _err_callback = CallBackDescriptor("_err_callback")

    def __init__(self, name: Union[str, Iterable[str]]):
        if isinstance(name, str):
            self.name = {name}
        elif isinstance(name, Iterable):
            self.name = set(name)
        self.sub: List[Self] = []
        self._tip: Optional[CallBack] = None
        self._func: Optional[CallBack] = None
        self._err_callback: Optional[CallBack] = None

        self._default_opts: List[CommandOption] = []
        self._default_args: List[CommandArgument] = []
        self._default_flags: List[CommandFlag] = []

        self._opt_groups: List[CommandOptionGroup] = []
        self._flag_groups: List[CommandFlagGroup] = []

    def __call__(self, *nodes) -> Self:
        self.sub += nodes
        return self

    def __repr__(self):
        attrs = (k for k in self.__dict__ if not (k.startswith("__") and k.endswith("__")))
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k in attrs if (v := self.__dict__[k]))})"

    def arg(self, name: str, types: Optional[Set[type]] = None, tip: Optional[str] = None) -> Self:
        """
        添加参数
        :param name: 名称
        :param types: 参数的类型
        :param tip: 帮助提示
        :return:
        """
        check_name(name)
        self._default_args.append(
            CommandArgument(name=name, types=types, tip=tip)
        )
        return self

    def opt(
            self,
            name: str,
            shortcuts: Optional[List[str]] = None,
            optional: bool = True,
            types: Optional[Set[type]] = None,
            tip: Optional[CallBack] = None
    ) -> Self:
        """
        添加选项
        :param name: 名称
        :param shortcuts: 快捷名
        :param optional: 是否可选
        :param types: 选项的类型
        :param tip: 帮助提示
        :return:
        """
        check_name(name)
        if shortcuts is not None and len(shortcuts) != 0:
            check_name(shortcuts)
        self._default_opts.append(
            CommandOption(name=name, shortcuts=shortcuts, optional=optional, types=types, tip=tip)
        )
        return self

    def opt_group(self, opts: List[CommandOption], optional: bool = False, exclusive: bool = False) -> Self:
        """
        添加选项组
        :param opts: 选项列表
        :param optional: 选项组是否可选
        :param exclusive: 选项组中的选项是否是互斥的
        :return:
        """
        self._opt_groups.append(
            CommandOptionGroup(options=opts, optional=optional, exclusive=exclusive)
        )
        return self

    def flag(self, name: str, shortcuts: Optional[List[str]] = None, tip: Optional[CallBack] = None) -> Self:
        """
        添加标志参数 ( --xxx|-x )
        :param name: 名称
        :param shortcuts: 快捷名称
        :param tip: 帮助提示
        :return:
        """
        check_name(name)
        if shortcuts is not None and len(shortcuts) != 0:
            check_name(shortcuts)
        self._default_flags.append(
            CommandFlag(name=name, shortcuts=shortcuts, tip=tip)
        )
        return self

    def flag_group(self, flags: List[CommandFlag], exclusive: bool = False) -> Self:
        """
        添加标志组
        :param flags: 标志列表
        :param exclusive: 标志组中的标志是否互斥
        :return:
        """
        self._flag_groups.append(
            CommandFlagGroup(flags=flags, exclusive=exclusive)
        )
        return self

    def error(self, callback: CallBack) -> Self:
        """
        添加错误回调函数
        :param callback:
        :return:
        """
        self._err_callback = callback
        return self

    def run(self, func: CallBack) -> Self:
        """
        添加回调函数
        :param func: 回调函数
        :return:
        """
        self._func = func
        return self

    def tip(self, tip: CallBack) -> Self:
        """
        添加提示
        :param tip: 提示
        :return:
        """
        self._tip = tip
        return self

    def _sub_parse(self, parsing: Parsed) -> Parsed:
        """
        当作为子节点时的命令解析
        :param parsing: 解析命令
        :return:
        """

    def _parse(self, cmd: str) -> Parsed:
        """
        解析单条命令
        :param cmd: 命令
        :return:
        """
        parsing = Parsed(original_text=cmd,
                         pointer=0,)
        first_ele = get_element(cmd)
        parsing.pointer = len(first_ele)
        if not first_ele == cmd:
            parsing.current_text = cmd[len(first_ele):]
        else:
            parsing.current_text = ""
        if first_ele in self.name:
            # match literal
            # match args
            # match flags
            # match opts
            ...
        else:
            return Parsed()

    def parse(self, cmd: Union[str, List[str]]) -> Parsed:
        """
        递归的解析命令
        :param cmd:
        :return:
        """
        ...

    def to_doc(self) -> str:
        ...
