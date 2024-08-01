<h1 align="center"><a href="https://rocketry.readthedocs.io">Tocketry</a></h1>
<h2 align="center">This code is currently a work in progress and not stable</h2>
<p align="center">
    <em>The fork of the engine to power your Python apps</em>
</p>

---

## What is it?

Tocketry is a fork of the project Rocketry created by [Miksus](https://github.com/Miksus)

Tocketry is a modern statement-based scheduling framework
for Python. It is simple, clean and extensive.
It is suitable for small and big projects.

Tocketry aims to be a lighter version of Rocketry without the need for pydantic as a dependency

This is how it looks like:

```python
from tocketry import Tocketry
from tocketry.conds import daily

app = Tocketry()

@app.task(daily)
def do_daily():
    ...

if __name__ == '__main__':
    app.run()
```

Core functionalities:

- Powerful scheduling
- Concurrency (async, threading, multiprocess)
- Parametrization
- Task pipelining
- Modifiable session also in runtime
- Async support

Links:

- Documentation: _Work in Progress_
- Source code: https://github.com/Jypear/tocketry
- Releases: _Work in Progress_

## Why Tocketry?

Unlike the alternatives, Tocketry's scheduler is
statement-based. Tocketry natively supports the
same scheduling strategies as the other options,
including cron and task pipelining, but it can also be
arbitrarily extended using custom scheduling statements.

Here is an example of custom conditions:

```python
from tocketry.conds import daily, time_of_week
from pathlib import Path

@app.cond()
def file_exists(file):
    return Path(file).exists()

@app.task(daily.after("08:00") & file_exists("myfile.csv"))
def do_work():
    ...
```

Tocketry is suitable for quick automation projects
and for larger scale applications. It does not make
assumptions of your project structure.

## Installation

Install Tocketry from _Work in Progress_

```shell
pip install tocketry
```

## More Examples

Here are some more examples of what it can do.

**Scheduling:**

```python
from tocketry.conds import every
from tocketry.conds import hourly, daily, weekly,
from tocketry.conds import time_of_day
from tocketry.conds import cron

@app.task(every("10 seconds"))
def do_continuously():
    ...

@app.task(daily.after("07:00"))
def do_daily_after_seven():
    ...

@app.task(hourly & time_of_day.between("22:00", "06:00"))
def do_hourly_at_night():
    ...

@app.task((weekly.on("Mon") | weekly.on("Sat")) & time_of_day.after("10:00"))
def do_twice_a_week_after_ten():
    ...

@app.task(cron("* 2 * * *"))
def do_based_on_cron():
    ...
```

**Pipelining tasks:**

```python
from tocketry.conds import daily, after_success
from tocketry.args import Return

@app.task(daily.after("07:00"))
def do_first():
    ...
    return 'Hello World'

@app.task(after_success(do_first))
def do_second(arg=Return('do_first')):
    # arg contains the value of the task do_first's return
    ...
    return 'Hello Python'
```

**Parallelizing tasks:**

```python
from tocketry.conds import daily

@app.task(daily, execution="main")
def do_unparallel():
    ...

@app.task(daily, execution="async")
async def do_async():
    ...

@app.task(daily, execution="thread")
def do_on_separate_thread():
    ...

@app.task(daily, execution="process")
def do_on_separate_process():
    ...
```

---

## Interested?

Read more from _Work in Progress_.

## About Library

- **Author and Maintainer:** Josh Pearson ([Jypear](https://github.com/Jypear))
- **Original Creator:** Mikael Koli ([Miksus](https://github.com/Miksus)) - koli.mikael@gmail.com
- **License:** MIT

