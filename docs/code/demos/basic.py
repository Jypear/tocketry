from tocketry import Tocketry

app = Tocketry()


@app.task("daily")
def do_things(): ...


@app.task("after task 'do_things'")
def do_after_things(): ...


if __name__ == "__main__":
    app.run()
