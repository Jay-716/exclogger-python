# exclogger

Trace ***any*** python exceptions and perform customizable actions.

Based on [python-hunter](https://github.com/ionelmc/python-hunter).

# Usage

```python
from logging import getLogger
from exclogger import (enable_exception_tracing, disable_exception_tracing,
                       LoggingExceptionHandler)

logger = getLogger()
enable_exception_tracing(LoggingExceptionHandler(logger))

try:
    raise ValueError("This is a test exception.")
except ValueError:
    pass

disable_exception_tracing()
```

# Config

All calls below are valid:

```python
# Use the default print handler, tracing all modules except stdlib
enable_exception_tracing()

# Use handler, tracing only foo module and stdlib
enable_exception_tracing(handler, stdlib=True, module="foo")

# Use handler, tracing only foo and bar module and stdlib
enable_exception_tracing(handler, stdlib=False, module=["foo", "bar"])
```

To customize actions on exceptions occur, inherit `BaseExceptionHandler`
and override method `__call__(self, excinfo: ExceptionInfo)`
