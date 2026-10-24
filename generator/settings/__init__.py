"""Every tunable number of the mod, one module per section of CHANGELOG.md.

Change a value in the module of its section, then run `python generator/generate.py` and
`scripts/install.ps1` to rebuild and install the mod.

The features read the settings as attributes of this package (`settings.ADMIN_BAR_MAX`): every
upper-case name of every module below is available here, and a name may only be defined once.
"""

from __future__ import annotations

from types import ModuleType

from . import (admin, ai, buildings, characters, confederations, difficulty, experience, garrisons, landmarks,
               movement, outposts, religion)

MODULES: list[ModuleType] = [admin, outposts, movement, landmarks, buildings, religion, garrisons, experience,
                             difficulty, ai, characters, confederations]


def _collect() -> dict[str, object]:
    values: dict[str, object] = {}
    defined_in: dict[str, str] = {}
    for module in MODULES:
        short = module.__name__.rsplit(".", 1)[-1]
        for name, value in vars(module).items():
            if not name.isupper():
                continue
            if name in defined_in:
                raise ValueError(f"Setting {name} is defined in both settings/{defined_in[name]}.py "
                                 f"and settings/{short}.py")
            defined_in[name] = short
            values[name] = value
    return values


globals().update(_collect())
