from tocketry import Tocketry
from tocketry.conds import daily

app = Tocketry()


@app.task(daily)
def do_things(): ...


if __name__ == "__main__":
    app.run()
