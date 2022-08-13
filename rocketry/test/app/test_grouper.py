
import asyncio
import logging

from rocketry import Rocketry, Grouper
from rocketry.conds import daily, time_of_day
from rocketry.args import Return, Arg, FuncArg
from redbird.logging import RepoHandler
from redbird.repos import MemoryRepo, CSVFileRepo

from rocketry import Session
from rocketry.tasks import CommandTask
from rocketry.tasks import FuncTask
from rocketry.conds import false, true

def set_logging_defaults():
    task_logger = logging.getLogger("rocketry.task")
    task_logger.handlers = []
    task_logger.setLevel(logging.WARNING)

def test_simple(session):
    set_logging_defaults()

    app = Rocketry()

    @app.task(daily)
    def do_things():
        ...

    group = Grouper()

    @group.task(daily)
    def do_other_things():
        ...

    assert app.session.tasks == {app.session["do_things"]}

    app.include_grouper(group)
    assert app.session.tasks == {app.session["do_things"], app.session["do_other_things"]}
    assert app.session["do_other_things"].start_cond == daily

def test_prefix(session):
    set_logging_defaults()

    app = Rocketry()

    @app.task(daily)
    def do_things():
        ...

    group = Grouper(prefix="mytests.")

    @group.task(daily)
    def do_things():
        ...

    app.include_grouper(group)
    assert app.session.tasks == {app.session["do_things"], app.session["mytests.do_things"]}

def test_start_cond(session):
    set_logging_defaults()

    app = Rocketry()
    group = Grouper(start_cond=time_of_day.between("10:00", "18:00"))

    @group.task(daily)
    def do_things():
        ...

    app.include_grouper(group)
    task = app.session[do_things]
    assert task.start_cond == daily & time_of_day.between("10:00", "18:00")

def test_execution(session):
    set_logging_defaults()

    app = Rocketry(config=dict(task_execution="process"))
    group = Grouper(execution="main")

    @group.task(daily, execution="thread")
    def do_things():
        ...

    @group.task(daily)
    def do_things_2():
        ...

    app.include_grouper(group)
    assert app.session[do_things].execution == "thread"
    assert app.session[do_things_2].execution == "main"

def test_custom_condition(session):
    set_logging_defaults()

    app = Rocketry()

    @app.cond()
    def is_foo():
        return True

    group = Grouper()

    @group.cond()
    def is_bar():
        return True

    @group.task(is_foo & is_bar)
    def do_things():
        ...

    app.include_grouper(group)
    assert app.session.tasks == {app.session["do_things"]}

def test_params(session):
    set_logging_defaults()

    app = Rocketry()
    app.params(x="hello", z="world")

    group = Grouper()
    group.params(x="hi", y="universe")

    app.include_grouper(group)
    assert dict(app.session.parameters) == {"x": "hi", "y": "universe", "z": "world"}

def test_func_param(session):
    set_logging_defaults()

    app = Rocketry()
    @app.param("x")
    def get_x():
        return "hello"

    group = Grouper()
    @group.param("y")
    def get_x():
        return "world"

    app.include_grouper(group)
    assert list(app.session.parameters.keys()) == ["x", "y"]