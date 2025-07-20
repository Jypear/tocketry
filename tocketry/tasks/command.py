import subprocess
from typing import List, Optional, Union
from dataclasses import dataclass, field

try:
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal

from tocketry.core.parameters.parameters import Parameters
from tocketry.core.task import Task


@dataclass(eq=False)
class CommandTask(Task):
    """Task that executes a command from
    shell/terminal.

    Parameters
    ----------
    command : str, list
        Command to execute.
    cwd : str, optional
        Sets the current directory before the child is executed.
    shell : bool, optional
        If true, the command will be executed through the shell.
    kwds_popen : dict, optional
        Keyword arguments to be passed to subprocess.Popen
    **kwargs : dict
        See :py:class:`tocketry.core.Task`

    Examples
    --------

    >>> from tocketry.tasks import CommandTask
    >>> task = CommandTask("python -m pip install tocketry", name="my_cmd_task_1")

    Or list of commands:

    >>> task = CommandTask(["python", "-m", "pip", "install", "tocketry"], name="my_cmd_task_2")
    """

    command: Union[str, List[str]] = None
    shell: bool = False
    cwd: Optional[str] = None
    kwds_popen: dict = field(default_factory=dict)
    argform: Optional[Literal["-", "--", "short", "long"]] = None

    def __init__(self, command=None, **kwargs):
        """Initialize CommandTask with command and other parameters"""
        # Extract CommandTask specific arguments before calling parent
        shell = kwargs.pop('shell', False)
        cwd = kwargs.pop('cwd', None)
        kwds_popen = kwargs.pop('kwds_popen', {})
        argform = kwargs.pop('argform', None)
        
        # Call parent initialization
        super().__init__(**kwargs)
        
        # Set our dataclass fields manually
        self.command = command
        self.shell = shell
        self.cwd = cwd
        self.kwds_popen = kwds_popen
        self.argform = argform
        
        # Handle field validation
        self._validate_argform()
    
    def _validate_argform(self):
        """Validate and transform argform"""
        self.argform = {
            "long": "--",
            "--": "--",
            "short": "-",
            "-": "-",
            None: "--",
        }[self.argform]

    def get_kwargs_popen(self) -> dict:
        kwargs = {
            "cwd": self.cwd,
            "shell": self.shell,
            "stdin": subprocess.PIPE,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
        }
        kwargs.update(self.kwds_popen)
        return kwargs


    def execute(self, **parameters):
        """Run the command."""
        command = self.command

        for param, val in parameters.items():
            if not param.startswith("-"):
                param = self.argform + param

            if isinstance(command, str):
                command += f' {param} "{val}"'
            else:
                command += [param] + [val]

        # https://stackoverflow.com/a/5469427/13696660
        pipe = subprocess.Popen(command, **self.get_kwargs_popen())
        try:
            outs, errs = pipe.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            # https://docs.python.org/3.3/library/subprocess.html#subprocess.Popen.communicate
            pipe.kill()
            outs, errs = pipe.communicate()
            raise

        return_code = pipe.returncode
        if return_code != 0:
            if hasattr(errs, "decode"):
                errs = errs.decode("utf-8", errors="ignore")
            raise OSError(f"Failed running command ({return_code}): \n{errs}")
        return outs

    def postfilter_params(self, params: Parameters):
        # Only allows the task specific parameters
        # for simplicity
        return params

    def get_default_name(self, command=None, **kwargs):
        if command is None:
            command = getattr(self, 'command', None)
        if command is None:
            return "unnamed_command"
        return command if isinstance(command, str) else " ".join(command)
