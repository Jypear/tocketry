import pytest
from tocketry.conditions.task.task import TaskStarted
from tocketry.core.condition.base import BaseCondition
from tocketry.tasks import FuncTask

from tocketry.conditions import FuncCond
from tocketry.conds import true


def run_succeeding():
    pass


@pytest.mark.parametrize("execution", ["main", "thread", "process"])
def test_func_cond_decorator(session, execution):
    @FuncCond(decor_return_func=False)
    def is_true():
        return True

    assert isinstance(is_true, BaseCondition)

    task_success = FuncTask(
        run_succeeding,
        start_cond=true & is_true,
        name="task success",
        execution=execution,
        session=session,
    )

    session.config.shut_cond = TaskStarted(task=task_success) >= 1
    session.start()

    n_success = task_success.logger.filter_by(action="run").count()
    assert n_success == 1
