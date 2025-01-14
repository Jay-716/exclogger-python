import inspect
from functools import reduce
from types import TracebackType
from typing import Callable, Optional, Collection

import hunter
from hunter import Q, Event, config
from hunter.actions import ColorStreamAction

from exctypes import ExceptionInfo
from handlers import BaseExceptionHandler


class ExceptionHandlerAction(ColorStreamAction):
    def __init__(
            self,
            exc_handler: Callable[[ExceptionInfo], None],
            stream=config.Default('stream', None),
            force_colors=config.Default('force_colors', False),
            force_pid=config.Default('force_pid', False),
            filename_alignment=config.Default('filename_alignment', 40),
            thread_alignment=config.Default('thread_alignment', 12),
            pid_alignment=config.Default('pid_alignment', 9),
            repr_limit=config.Default('repr_limit', 1024),
            repr_func=config.Default('repr_func', 'safe_repr'),
    ):
        super().__init__(
            stream,
            force_colors,
            force_pid,
            filename_alignment,
            thread_alignment,
            pid_alignment,
            repr_limit,
            repr_func,
        )
        self.exc_handler = exc_handler

    def __call__(self, event: Event):
        if event.kind == "exception":
            tb: TracebackType = event.arg[2]
            if tb and not tb.tb_next:
                # The next traceback frame is None, which indicates that this is the last frame.
                # In other words, this function is where the exception occurs.
                self.exc_handler(
                    ExceptionInfo(
                        event.filename, event.lineno,
                        event.function, inspect.getargvalues(event.frame),
                        event.arg[1],
                        event.frame,
                        event.arg[2],
                    )
                )


def enable_exception_tracing(
        exc_handler: Optional[BaseExceptionHandler] = None,
        stdlib: bool = False,
        module: Optional[str | Collection[str]] = None,
) -> None:
    predicate = Q(stdlib=stdlib) & Q(kind="exception")
    if module:
        if isinstance(module, str) and module:
            predicate &= Q(module=module)
        elif isinstance(module, Collection) and len(module) > 0:
            qs = [Q(module=mod) for mod in module]
            predicate &= reduce(lambda lhs, rhs: lhs | rhs, qs)
    hunter.trace(predicate,
                 action=ExceptionHandlerAction(exc_handler if exc_handler else BaseExceptionHandler()))


def disable_exception_tracing() -> None:
    hunter.stop()
