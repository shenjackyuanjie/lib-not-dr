from dataclasses import field
from typing import Set, List, Optional
from lib_not_dr.types.options import Options


class Parsed:
    ...


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
