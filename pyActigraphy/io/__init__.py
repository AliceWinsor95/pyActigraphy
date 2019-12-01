"""IO module for reading raw data."""

# Authors: Grégory Hammad <gregory.hammad@uliege.be>
#
# License: BSD (3-clause)

# from . import awd
# from . import rpx
# from . import reader

from .base import BaseRaw
from .reader import RawReader

from .reader import read_raw
from .agd import read_raw_agd
from .awd import read_raw_awd
from .dqt import read_raw_dqt
from .mtn import read_raw_mtn
from .rpx import read_raw_rpx

__all__ = [
    "BaseRaw", "RawReader",
    "read_raw",
    "read_raw_agd",
    "read_raw_awd",
    "read_raw_dqt",
    "read_raw_mtn",
    "read_raw_rpx"
]
