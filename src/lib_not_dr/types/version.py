# 本文件以 GNU Lesser General Public License v3.0（GNU LGPL v3) 开源协议进行授权 (谢谢狐狸写出这么好的MCDR)
# 顺便说一句,我把所有的tab都改成了空格,因为我觉得空格比tab更好看(草,后半句是github copilot自动填充的)

"""
This part of code come from MCDReforged(https://github.com/Fallen-Breath/MCDReforged)
Thanks a lot to Fallen_Breath and MCDR contributors
GNU Lesser General Public License v3.0 (GNU LGPL v3)
"""

import re
from typing import List, Callable, Tuple, Optional, Union
"""
Plugin Version
"""


# beta.3 -> (beta, 3), random -> (random, None)
class ExtraElement:
    DIVIDER = '.'
    body: str
    num: Optional[int]

    def __init__(self, segment_str: str):
        segments = segment_str.rsplit(self.DIVIDER, 1)
        try:
            self.body, self.num = segments[0], int(segments[1])
        except (IndexError, ValueError):
            self.body, self.num = segment_str, None

    def __str__(self):
        if self.num is None:
            return self.body
        return '{}{}{}'.format(self.body, self.DIVIDER, self.num)

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError()
        if self.num is None or other.num is None:
            return str(self) < str(other)
        else:
            return (self.body, self.num) < (other.body, other.num)


class Version:
    """
    A version container that stores semver like version string

    Example:

    * ``"1.2.3"``
    * ``"1.0.*"``
    * ``"1.2.3-pre4+build.5"``
    """
    EXTRA_ID_PATTERN = re.compile(r'|[-+0-9A-Za-z]+(\.[-+0-9A-Za-z]+)*')
    WILDCARDS = ('*', 'x', 'X')
    WILDCARD = -1

    component: List[int]
    has_wildcard: bool
    pre: Optional[ExtraElement]
    build: Optional[ExtraElement]

    def __init__(self, version_str: str, *, allow_wildcard: bool = True):
        """
        :param version_str: The version string to be parsed
        :keyword allow_wildcard: If wildcard (``"*"``, ``"x"``, ``"X"``) is allowed. Default: ``True``
        """
        if not isinstance(version_str, str):
            raise VersionParsingError('Invalid input version string')

        def separate_extra(text, char) -> Tuple[str, Optional[ExtraElement]]:
            if char in text:
                text, extra_str = text.split(char, 1)
                if not self.EXTRA_ID_PATTERN.fullmatch(extra_str):
                    raise VersionParsingError('Invalid build string: ' + extra_str)
                extra = ExtraElement(extra_str)
            else:
                extra = None
            return text, extra

        self.component = []
        self.has_wildcard = False
        version_str, self.build = separate_extra(version_str, '+')
        version_str, self.pre = separate_extra(version_str, '-')
        if len(version_str) == 0:
            raise VersionParsingError('Version string is empty')
        for comp in version_str.split('.'):
            if comp in self.WILDCARDS:
                self.component.append(self.WILDCARD)
                self.has_wildcard = True
                if not allow_wildcard:
                    raise VersionParsingError('Wildcard {} is not allowed'.format(comp))
            else:
                try:
                    num = int(comp)
                except ValueError:
                    num = None
                if num is None:
                    raise VersionParsingError('Invalid version number component: {}'.format(comp))
                if num < 0:
                    raise VersionParsingError('Unsupported negatived number component: {}'.format(num))
                self.component.append(num)
        if len(self.component) == 0:
            raise VersionParsingError('Empty version string')

    def __str__(self):
        version_str = '.'.join(map(lambda c: str(c) if c != self.WILDCARD else self.WILDCARDS[0], self.component))
        if self.pre is not None:
            version_str += '-' + str(self.pre)
        if self.build is not None:
            version_str += '+' + str(self.build)
        return version_str

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index: int) -> int:
        if index < len(self.component):
            return self.component[index]
        else:
            return self.WILDCARD if self.component[len(self.component) - 1] == self.WILDCARD else 0

    def __lt__(self, other):
        if not isinstance(other, Version):
            raise TypeError('Cannot compare between instances of {} and {}'.format(Version.__name__, type(other).__name__))
        for i in range(max(len(self.component), len(other.component))):
            if self[i] == self.WILDCARD or other[i] == self.WILDCARD:
                continue
            if self[i] != other[i]:
                return self[i] < other[i]
        if self.pre is not None and other.pre is not None:
            return self.pre < other.pre
        elif self.pre is not None:
            return not other.has_wildcard
        elif other.pre is not None:
            return False
        else:
            return False

    def __eq__(self, other):
        return not self < other and not other < self

    def __le__(self, other):
        return self == other or self < other

    def compare_to(self, other):
        if self < other:
            return -1
        elif self > other:
            return 1
        else:
            return 0


DEFAULT_CRITERION_OPERATOR = '='


class Criterion:
    def __init__(self, opt: str, base_version: Version, criterion: Callable[[Version, Version], bool]):
        self.opt = opt
        self.base_version = base_version
        self.criterion = criterion

    def test(self, target: Union[Version, str]):
        return self.criterion(self.base_version, target)

    def __str__(self):
        return '{}{}'.format(self.opt if self.opt != DEFAULT_CRITERION_OPERATOR else '', self.base_version)


class VersionRequirement:
    """
    A version requirement tester

    It can test if a given :class:`Version` object matches its requirement
    """
    CRITERIONS = {
        '<=': lambda base, ver: ver <= base,
        '>=': lambda base, ver: ver >= base,
        '<': lambda base, ver: ver < base,
        '>': lambda base, ver: ver > base,
        '=': lambda base, ver: ver == base,
        '^': lambda base, ver: ver >= base and ver[0] == base[0],
        '~': lambda base, ver: ver >= base and ver[0] == base[0] and ver[1] == base[1],
    }

    def __init__(self, requirements: str):
        """
        :param requirements: The requirement string, which contains several version predicates connected by space character.
            e.g. ``">=1.0.x"``, ``"^2.9"``, ``">=1.2.0 <1.4.3"``
        """
        if not isinstance(requirements, str):
            raise VersionParsingError('Requirements should be a str, not {}'.format(type(requirements).__name__))
        self.criterions = []  # type: List[Criterion]
        for requirement in requirements.split(' '):
            if len(requirement) > 0:
                for prefix, func in self.CRITERIONS.items():
                    if requirement.startswith(prefix):
                        opt = prefix
                        base_version = requirement[len(prefix):]
                        break
                else:
                    opt = DEFAULT_CRITERION_OPERATOR
                    base_version = requirement
                self.criterions.append(Criterion(opt, Version(base_version), self.CRITERIONS[opt]))

    def accept(self, version: Union[Version, str]):
        if isinstance(version, str):
            version = Version(version)
        for criterion in self.criterions:
            if not criterion.test(version):
                return False
        return True

    def __str__(self):
        return ' '.join(map(str, self.criterions))


class VersionParsingError(ValueError):
    pass
