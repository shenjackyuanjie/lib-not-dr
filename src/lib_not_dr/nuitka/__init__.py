#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import TYPE_CHECKING, Dict, Union, List, Callable

if TYPE_CHECKING:
    from lib_not_dr.nuitka import reader, compile

nuitka_config_type = Dict[str, Union[str, bool, List[Union[str, tuple]]]]
raw_config_type = Dict[str, Union[nuitka_config_type, str]]
parse_config_function = Callable[[raw_config_type], nuitka_config_type]

# fmt: off
__all__ = [
    "reader",
    "compile",
    "raw_config_type",
    "parse_config_function",
    "nuitka_config_type"
]
# fmt: on

