#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

__version__ = '0.2.0-beta.3'

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib_not_dr import (
        logger,
        nuitka,
        types,
        command
    )

__all__ = [
    '__version__',
    'logger',
    'nuitka',
    'types',
    'command'
]
