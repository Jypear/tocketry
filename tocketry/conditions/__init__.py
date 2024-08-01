from functools import partial

from tocketry.time.interval import TimeOfHour, TimeOfMinute, TimeOfMonth
from tocketry.core.condition import (
    AlwaysFalse,
    AlwaysTrue,
    All,
    Any,
    Not,
    BaseCondition,
)
from .func import FuncCond
from .task import *
from .scheduler import *
from .time import *
from .parameter import ParamExists, IsEnv
from .meta import TaskCond
