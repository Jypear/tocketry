import sys
import inspect
import importlib
from pathlib import Path
from typing import Callable, List, Optional
import warnings
from dataclasses import dataclass, field

from tocketry.core.task import Task
from tocketry.core.parameters import Parameters
from tocketry.pybox.pkg import find_package_root


def get_module(path, pkg_path=None):
    if pkg_path:
        name = ".".join(
            path.with_suffix(
                ""
            ).parts[  # path/to/file/myfile.py --> path.to.file.myfile
                len(pkg_path.parts) :
            ]  # root/myproject/pkg/myfile.py --> myproject.pkg.myfile
        )
    else:
        name = Path(path).name

    spec = importlib.util.spec_from_file_location(name, Path(path).absolute())
    task_module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(task_module)
    except Exception as exc:
        raise ImportError(f"Importing the file '{path}' failed.") from exc
    return task_module


class TempSysPath:
    # TODO: To utils.
    sys_path = sys.path

    def __init__(self, paths: list):
        self.paths = paths

    def __enter__(self):
        for path in self.paths:
            sys.path.append(path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for path in self.paths:
            try:
                self.sys_path.remove(path)
            except ValueError:
                pass


@dataclass(eq=False)
class FuncTask(Task):
    """Task that executes a function or callable.

    Parameters
    ----------
    func : Callable, str
        Function or name of a function to be executed. If string is
        passed, the path to the file where the function is should
        be passed with ``path`` or in the argument, like
        "path/to/file.py:my_func".
    path : path-like
        Path to the function. Not needed if ``func`` is callable.
    delay : bool, optional
        If True, the function is imported and set to the task
        immediately. If False, the function is imported only
        when running the task. By default False if ``func`` is
        callable and True if ``func`` is a name of a function.
    sys_path : list of paths
        Paths that are appended to ``sys.path`` when the function
        is imported.
    **kwargs : dict
        See :py:class:`tocketry.core.Task`


    Examples
    --------

    >>> from tocketry.tasks import FuncTask
    >>> def myfunc():
    ...     ...
    >>> task = FuncTask(myfunc, name="my_func_task_1")

    **Via decorator:**

    >>> from tocketry.tasks import FuncTask
    >>> @FuncTask(name='my_func_task_2', start_cond="daily")
    ... def myfunc():
    ...     ...

    If the ``name`` is not defined, the name will be in form
    ``path.to.module:myfunc``.

    Or from string using lazy importing:

    >>> from tocketry.tasks import FuncTask
    >>> task = FuncTask("myfunc", path="path/to/script.py", name='my_func_task_3', start_cond="daily")

    Warnings
    --------

    If ``execution='process'``, only picklable functions can be used.
    The following will NOT work:

    .. code-block:: python

        # Lambda functions are not allowed
        FuncTask(lambda:None, execution="process")

    .. code-block:: python

        # nested functions are not allowed
        def my_func():
            @FuncTask(execution="process")
            def my_task_func():
                ...
        my_func()

    .. code-block:: python

        def my_decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        # decorated functions are not allowed
        @my_decorator
        @FuncTask(execution="process")
        def my_task_func():
            ...
    """

    func: Optional[Callable] = None
    path: Optional[Path] = None
    func_name: str = "main"
    cache: bool = False
    sys_paths: List[Path] = field(default_factory=list)
    
    # Private attributes (equivalent to PrivateAttr)
    _is_delayed: bool = field(default=False, init=False)
    _delayed_kwargs: dict = field(default_factory=dict, init=False)
    _name_template: str = field(default="{module_name}:{func_name}", init=False)

    @property
    def delayed(self):
        return self._is_delayed

    def __post_init__(self):
        """Validate fields after initialization"""
        # Call parent's __post_init__ first
        super().__post_init__()
        
        # Validate path
        if self.path is not None and not self.path.is_file():
            warnings.warn(f"Path {self.path} does not exists. Task '{self.name}' may fail.")

    def __init__(self, func=None, **kwargs):
        only_func_set = func is not None and not kwargs
        no_func_set = func is None and kwargs.get("path") is None
        
        # Extract FuncTask specific arguments before calling parent
        path = kwargs.pop('path', None)
        func_name = kwargs.pop('func_name', 'main')
        cache = kwargs.pop('cache', False)
        sys_paths = kwargs.pop('sys_paths', [])
        
        if no_func_set:
            # FuncTask was probably called like:
            # @FuncTask(...)
            # def myfunc(...): ...

            # We initiate the class lazily by creating
            # almost empty shell class that is populated
            # in next __call__ (which should occur immediately)
            self._delayed_kwargs = dict(func=func, path=path, func_name=func_name, cache=cache, sys_paths=sys_paths, **kwargs)
            # Call parent with empty kwargs for delayed init
            super().__init__(**kwargs)
            # Set our specific fields
            self.func = None
            self.path = None
            self.func_name = 'main'
            self.cache = False
            self.sys_paths = []
            self._is_delayed = True
            self._name_template = "{module_name}:{func_name}"
            return
            
        if only_func_set:
            # Most likely called as:
            # @FuncTask
            # def myfunc(...): ...

            # We are slightly forgiving and set
            # the execution to else than process
            # as it's obvious it would not work.
            kwargs["execution"] = "thread"

        # Call parent initialization (keep func in kwargs for name generation)
        super().__init__(func=func, **kwargs)
        
        # Set our dataclass fields manually
        self.func = func
        self.path = path
        self.func_name = func_name
        self.cache = cache
        self.sys_paths = sys_paths
        self._is_delayed = False
        self._delayed_kwargs = {}
        self._name_template = "{module_name}:{func_name}"
        
        # Validate func for process execution
        if self.execution == "process" and getattr(self.func, "__name__", None) == "<lambda>":
            raise AttributeError(
                f"Cannot pickle lambda function '{self.func}'. "
                "The function must be pickleable if task's execution is 'process'. "
            )
        
        self._set_descr(is_delayed=func is None)

    def __call__(self, *args, **kwargs):
        if self.func is None and self._delayed_kwargs:
            func = args[0]
            
            # Extract FuncTask specific kwargs from delayed_kwargs
            delayed = self._delayed_kwargs
            self.func = func
            self.path = delayed.get('path')
            self.func_name = delayed.get('func_name', 'main') 
            self.cache = delayed.get('cache', False)
            self.sys_paths = delayed.get('sys_paths', [])
            
            # Update the task name with the actual function name only if no explicit name was provided
            old_name = self.name
            explicit_name = delayed.get('name')  # Check if explicit name was provided
            
            # Only update name if no explicit name was provided and using a temporary name
            if explicit_name is None and old_name.startswith('delayed_task_'):
                _name_template = delayed.get('_name_template', "{module_name}:{func_name}")
                if 'name_include_module' in delayed and not delayed['name_include_module']:
                    # Just use function name without module
                    new_name = func.__name__
                else:
                    # Use the standard naming pattern
                    new_name = self.get_default_name(
                        func=func, 
                        _name_template=_name_template
                    )
                
                # Update name and re-register if needed
                if new_name != old_name:
                    # Remove old registration
                    if hasattr(self.session, 'tasks') and self in self.session.tasks:
                        self.session.tasks.remove(self)
                    
                    # Update name 
                    self.name = new_name
                    
                    # Re-register with new name
                    if hasattr(self.session, 'tasks'):
                        self.session.tasks.add(self)
            
            self._set_descr(is_delayed=False)
            self._delayed_kwargs = {}

            # Note that we must return the function or
            # we are in deep shit with multiprocessing
            # (or pickling the function).

            # As we return the function, the name of the
            # task might be missing. We set the name so
            # that condition API can identify the name.
            # If the task is renamed, the link is lost. (TODO)
            func.__tocketry__ = {"name": self.name}

            return func
        return super().__call__(*args, **kwargs)

    def _set_descr(self, is_delayed: bool):
        "Set description from func doc if desc missing"
        if self.func is not None and self.description is None and hasattr(self.func, "__doc__"):
            self.description = self.func.__doc__
        # Set params
        if not is_delayed and self.func is not None:
            # Not-delayed, setting parameters from the
            # function signature
            params = Parameters._from_signature(self.func)
            self.parameters = params | self.parameters
        self._is_delayed = is_delayed

    async def execute(self, **params):
        "Run the actual, given, task"
        func = self.get_func(cache=self.cache)

        is_async = inspect.iscoroutinefunction(func)
        if is_async:
            output = await func(**params)
        else:
            output = func(**params)
        return output

    def get_func(self, cache=True):
        if self.func is None:
            # Add dir of self.path to sys.path so importing from that dir works
            pkg_path = find_package_root(self.path)
            root = (
                str(Path(self.path).parent.absolute())
                if not pkg_path
                else str(pkg_path)
            )

            # _task_func is cached to faster performance
            with TempSysPath([root] + self.sys_paths):
                task_module = get_module(self.path, pkg_path=pkg_path)
            task_func = getattr(task_module, self.func_name)

            if cache:
                self.func = task_func
            return task_func
        return self.func

    def get_default_name(
        self, func=None, path=None, func_name=None, _name_template=None, name=None, **kwargs
    ):
        if func is None:
            if path is None:
                # For delayed tasks, use a unique temporary name
                if hasattr(self, '_delayed_kwargs') and self._delayed_kwargs:
                    return f"delayed_task_{id(self)}"
                # Make unnamed tasks unique to avoid naming conflicts
                return f"unnamed_task_{id(self)}"
            file = Path(path)
            module_name = ".".join(file.parts).replace(".py", "")
        else:
            module_name = func.__module__
            func_name = getattr(func, "__name__", type(func).__name__)
            if module_name == "__main__":
                # Showing as 'myfunc'
                return func_name
        if _name_template is not None:
            return _name_template.format(module_name=module_name, func_name=func_name)
        return f"{module_name}:{func_name}"

    def process_finish(self, *args, **kwargs):
        if self._is_delayed:
            # Deleting the _func so it is refreshed
            # next time the task is run.
            self.func = None
        super().process_finish(*args, **kwargs)

    def is_delayed(self):
        return self._is_delayed

    def get_task_params(self):
        task_params = super().get_task_params()

        if self._is_delayed:
            # Get params from the typehints
            cache = self.path is None
            func = self.get_func(cache=cache)
            func_params = Parameters._from_signature(
                func, task=self, session=self.session
            )
            params = func_params | task_params
        else:
            params = task_params
        return params

    def prefilter_params(self, params):
        if not self.is_delayed():
            # Filter the parameters now so that
            # we pass as little as possible to
            # pickling. If lazy, we filter after
            # pickling to handle problems in
            # pickling functions.
            return {key: val for key, val in params.items() if key in self.kw_args}
        return params

    def postfilter_params(self, params: Parameters):
        if self._is_delayed:
            # Was not filtered in prefiltering.
            return {key: val for key, val in params.items() if key in self.kw_args}
        return params

    @property
    def pos_args(self):
        func = self.get_func()
        sig = inspect.signature(func)
        pos_args = [
            val.name
            for name, val in sig.parameters.items()
            if val.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,  # NOTE: Python <= 3.8 do not have positional arguments, but maybe in the future?
                inspect.Parameter.POSITIONAL_OR_KEYWORD,  # Keyword argument
            )
        ]
        return pos_args

    @property
    def kw_args(self):
        func = self.get_func()
        sig = inspect.signature(func)
        kw_args = [
            val.name
            for name, val in sig.parameters.items()
            if val.kind
            in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,  # Normal argument
                inspect.Parameter.KEYWORD_ONLY,  # Keyword argument
            )
        ]
        return kw_args
