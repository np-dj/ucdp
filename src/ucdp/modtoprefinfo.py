#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""Module Reference Information."""

from inspect import getfile
from pathlib import Path
from typing import Literal

from .mod import AMod
from .modbase import BaseMod, ModCls, ModTags
from .modconfigurable import AConfigurableMod
from .modcore import ACoreMod
from .modtailored import ATailoredMod
from .modtb import AGenericTbMod, ATbMod
from .modtopref import TopModRef
from .object import Object

BASECLSS = (AConfigurableMod, ACoreMod, ATailoredMod, AMod, AGenericTbMod, ATbMod, BaseMod)


TbType = Literal["Static", "Generic", ""]


class TopModRefInfo(Object):
    """Module Reference Information."""

    topmodref: TopModRef
    tags: ModTags
    modbasecls: ModCls
    filepath: Path
    is_top: bool
    tb: TbType

    @staticmethod
    def create(topmodref: TopModRef, modcls: ModCls) -> "TopModRefInfo":
        """Create."""
        return TopModRefInfo(
            topmodref=topmodref,
            tags=modcls.tags,
            modbasecls=get_modbasecls(modcls),
            filepath=Path(getfile(modcls)),
            is_top=is_top(modcls),
            tb=get_tb(modcls),
        )


def get_modbasecls(modcls: ModCls) -> type[BaseMod] | None:
    """Determine Module Base Class."""
    for basecls in BASECLSS:
        if issubclass(modcls, basecls):
            return basecls
    return None  # pragma: no cover


def is_top(modcls: ModCls) -> bool:
    """Module is Direct Loadable."""
    if issubclass(modcls, AGenericTbMod):
        return modcls.build_dut.__qualname__ != AGenericTbMod.build_dut.__qualname__
    if issubclass(modcls, (AConfigurableMod, AMod, ATbMod)):
        return True
    return False


def get_tb(modcls: ModCls) -> TbType:
    """Module Testbench."""
    if issubclass(modcls, AGenericTbMod):
        return "Generic"
    if issubclass(modcls, ATbMod):
        return "Static"
    return ""
