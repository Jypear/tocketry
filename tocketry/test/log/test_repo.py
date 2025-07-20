import logging

import pytest
from tocketry.repo import RepoHandler, MemoryRepo
from tocketry import Tocketry
from tocketry.log import MinimalRecord, MinimalRunRecord, TaskLogRecord, TaskRunRecord


def get_csv(model, tmpdir):
    # CSV repo removed - use MemoryRepo for testing
    return MemoryRepo(model=model)


def get_sql(model, tmpdir):
    # SQL repo removed - use MemoryRepo for testing  
    return MemoryRepo(model=model)


@pytest.mark.parametrize("get_repo", [get_csv, get_sql])
@pytest.mark.parametrize(
    "model", [MinimalRecord, MinimalRunRecord, TaskLogRecord, TaskRunRecord]
)
def test_cache(session, tmpdir, model, get_repo):
    # Version check removed since redbird is no longer used
    repo = get_repo(model=model, tmpdir=tmpdir)
    task_logger = logging.getLogger(session.config.task_logger_basename)
    task_logger.handlers = [
        RepoHandler(repo=repo),
        # logging.StreamHandler(sys.stdout)
    ]

    task = session.create_task(func=lambda: None, name="task 1")
    task.log_running()
    task.log_success()

    task.set_cached()

    logs = repo.filter_by().all()
    logs = [{"action": r.action, "task_name": r.task_name} for r in logs]
    assert task.status == "success"
    assert logs == [
        {"action": "run", "task_name": "task 1"},
        {"action": "success", "task_name": "task 1"},
    ]
