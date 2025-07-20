from tocketry.core import BaseCondition, Task

from tocketry.session import Session, Config
from tocketry.parse import add_condition_parser
from tocketry.conds import true, false
from tocketry.tasks import CommandTask, FuncTask, CodeTask, _DummyTask
from tocketry.tasks.maintain import ShutDown, Restart

from tocketry.conditions.meta import _FuncTaskCondWrapper


def _setup_defaults():
    "Set up the task classes and conditions tocketry provides out-of-the-box"

    # Add some extra parsers from core
    add_condition_parser(
        {"true": true, "false": false, "always false": false, "always true": true}
    )

    # Update type hints for remaining pydantic models
    cls_tasks = (
        Task,
        FuncTask,
        CommandTask,
        CodeTask,
        ShutDown,
        Restart,
        _DummyTask,
        _FuncTaskCondWrapper,
    )
    for cls_task in cls_tasks:
        # Skip model_rebuild for non-pydantic classes (Config is now a dataclass)
        if hasattr(cls_task, 'model_rebuild'):
            cls_task.model_rebuild(
                force=True,
                _types_namespace={"Session": Session, "BaseCondition": BaseCondition},
                _parent_namespace_depth=4,
            )

    # Config is now a dataclass, no model_rebuild needed
    # Session.update_forward_refs(
    #    Task=Task, Parameters=Parameters, Scheduler=Scheduler
    # )
