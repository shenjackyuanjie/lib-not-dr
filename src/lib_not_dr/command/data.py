import re
from dataclasses import field
from typing import Set, List, Optional, Any, Union, Callable
from lib_not_dr.types.options import Options


CallBack = Union[Callable[["Parsed"], Any], str]  # Equals to `Callable[[str], None] | str`
# 可调用对象或字符串作为回调
# A callable or str as callback

ParseArgFunc = Callable[[str], Optional[type]]
# 解析参数的函数，返回值为 None 时表示解析失败
# function to parse argument, return None when failed

EMPTY_WORDS = re.compile(r"\s", re.I)


class Parsed(Options):
    original_text: str
    pointer: int = 0
    current_text: str
    args: List[str] = []
    opts: List[str] = []
    flags: List[str] = []
    result: Optional[CallBack] = None

    def init(self, **kwargs) -> bool:
        if not hasattr(self, 'current_text'):
            self.current_text = self.original_text
        return False


class CommandOption(Options):
    name: str
    shortcuts: List[str]
    optional: bool
    types: Set[type] = field(default_factory=lambda: {str})
    tip: Optional[str] = None


class CommandOptionGroup(Options):
    options: List[CommandOption]
    optional: bool = True
    exclusive: bool = False


class CommandArgument(Options):
    name: str
    types: Set[type] = field(default_factory=lambda: {str})
    tip: Optional[str] = None


class CommandFlag(Options):
    name: str
    shortcuts: List[str]
    tip: Optional[str] = None


class CommandFlagGroup(Options):
    flags: List[CommandFlag]
    exclusive: bool = False
