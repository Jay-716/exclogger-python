import inspect
import traceback
from logging import Logger

from exctypes import ExceptionInfo


class BaseExceptionHandler:
    """
    The exception handler callable. This is called when an exception occurs.

    Override __call__ to customize.
    """
    def __init__(self):
        pass

    def __call__(self, excinfo: ExceptionInfo):
        print(f"{excinfo.filename}:{excinfo.lineno} {excinfo.func_name}{inspect.formatargvalues(*excinfo.func_args)}")
        traceback.print_tb(excinfo.tb)


class LoggingExceptionHandler(BaseExceptionHandler):
    """
    This handler simply logs all exceptions, together with position, function name, args, and full stacktrace.
    """

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def __call__(self, excinfo: ExceptionInfo):
        self.logger.warning(
            f"{excinfo.filename}:{excinfo.lineno} {excinfo.func_name}{inspect.formatargvalues(*excinfo.func_args)}",
            exc_info=(type(excinfo.exc), excinfo.exc , excinfo.tb)
        )
