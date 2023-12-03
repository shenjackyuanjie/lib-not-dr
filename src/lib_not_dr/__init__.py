#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

_version_ = "0.3.0-alpha.0"

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib_not_dr import logger, nuitka, types, command

# fmt: off
__all__ = [
    "_version_",
    "logger",
    "nuitka",
    "types",
    "command"
]
# fmt: on
