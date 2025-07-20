import datetime
from typing import Optional
from dataclasses import dataclass

from tocketry.pybox.time import to_datetime, to_timedelta


@dataclass
class MinimalRecord:
    """A log record with minimal number of fields for Tocketry to work"""

    task_name: str = ""
    action: str = ""  # Scheduler action: 'run', 'success', 'fail'
    created: float = 0.0

    def __init__(self, task_name="", action="", created=0.0, **kwargs):
        # Accept extra kwargs but only use the ones we need (like pydantic extra="ignore")
        self.task_name = task_name
        self.action = action
        self.created = created

    def model_dump(self):
        """Compatibility method to replace pydantic's model_dump"""
        from dataclasses import asdict
        return asdict(self)

    def __iter__(self):
        """Make dataclass compatible with dict(**item) calls"""
        from dataclasses import asdict
        return iter(asdict(self))

    def keys(self):
        """Make dataclass compatible with mapping protocol"""
        from dataclasses import asdict
        return asdict(self).keys()

    def values(self):
        """Make dataclass compatible with mapping protocol"""
        from dataclasses import asdict
        return asdict(self).values()

    def items(self):
        """Make dataclass compatible with mapping protocol"""
        from dataclasses import asdict
        return asdict(self).items()

    def __getitem__(self, key):
        """Make dataclass compatible with mapping protocol"""
        from dataclasses import asdict
        return asdict(self)[key]

    def __init_subclass__(cls, **kwargs):
        """Set model_fields on class creation for pydantic compatibility"""
        super().__init_subclass__(**kwargs)
        from dataclasses import fields
        cls.model_fields = {field.name: field for field in fields(cls)}

# Set model_fields for the base class itself
from dataclasses import fields
MinimalRecord.model_fields = {field.name: field for field in fields(MinimalRecord)}


@dataclass
class LogRecord(MinimalRecord):
    """A logging record

    See attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes
    """

    name: str = ""
    msg: str = ""
    levelname: str = ""
    levelno: int = 0
    pathname: str = ""
    filename: str = ""
    module: str = ""
    exc_text: Optional[str] = None  # Exception text
    lineno: int = 0
    funcName: str = ""
    msecs: float = 0.0
    relativeCreated: float = 0.0
    thread: int = 0
    threadName: str = ""
    processName: str = ""
    process: int = 0
    message: str = ""

    formatted_message: str = ""  # Formatted message. This field is created by RepoHandler.

    def __init__(self, task_name="", action="", created=0.0, 
                 name="", msg="", levelname="", levelno=0, pathname="", filename="", 
                 module="", exc_text=None, lineno=0, funcName="", msecs=0.0, 
                 relativeCreated=0.0, thread=0, threadName="", processName="", 
                 process=0, message="", formatted_message="", **kwargs):
        # Call parent constructor
        super().__init__(task_name, action, created, **kwargs)
        # Set LogRecord-specific fields
        self.name = name
        self.msg = msg
        self.levelname = levelname
        self.levelno = levelno
        self.pathname = pathname
        self.filename = filename
        self.module = module
        self.exc_text = exc_text
        self.lineno = lineno
        self.funcName = funcName
        self.msecs = msecs
        self.relativeCreated = relativeCreated
        self.thread = thread
        self.threadName = threadName
        self.processName = processName
        self.process = process
        self.message = message
        self.formatted_message = formatted_message


@dataclass
class TaskLogRecord(MinimalRecord):
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    runtime: Optional[datetime.timedelta] = None

    message: str = ""
    exc_text: Optional[str] = None

    def __init__(self, task_name="", action="", created=0.0, 
                 start=None, end=None, runtime=None, message="", exc_text=None, **kwargs):
        # Call parent constructor
        super().__init__(task_name, action, created, **kwargs)
        # Set TaskLogRecord-specific fields with validation
        self.start = to_datetime(start) if start is not None and not isinstance(start, datetime.datetime) else start
        self.end = to_datetime(end) if end is not None and not isinstance(end, datetime.datetime) else end
        self.runtime = to_timedelta(runtime) if runtime is not None and not isinstance(runtime, datetime.timedelta) else runtime
        self.message = message
        self.exc_text = exc_text


@dataclass
class MinimalRunRecord(MinimalRecord):
    run_id: Optional[str] = None

    def __init__(self, task_name="", action="", created=0.0, run_id=None, **kwargs):
        super().__init__(task_name, action, created, **kwargs)
        self.run_id = run_id


@dataclass
class RunRecord(LogRecord):
    run_id: Optional[str] = None

    def __init__(self, task_name="", action="", created=0.0, run_id=None, **kwargs):
        super().__init__(task_name, action, created, **kwargs)
        self.run_id = run_id


@dataclass
class TaskRunRecord(TaskLogRecord):
    run_id: Optional[str] = None

    def __init__(self, task_name="", action="", created=0.0, run_id=None, **kwargs):
        super().__init__(task_name, action, created, **kwargs)
        self.run_id = run_id
