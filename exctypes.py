from inspect import ArgInfo
from dataclasses import dataclass
from types import FrameType, TracebackType


@dataclass
class ExceptionInfo:
    filename: str
    lineno: str
    func_name: str
    func_args: ArgInfo
    exc: BaseException
    frame: FrameType
    tb: TracebackType
