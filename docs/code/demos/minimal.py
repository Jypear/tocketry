from tocketry import Tocketry

app = Tocketry()


@app.task("daily")
def do_things(): ...


if __name__ == "__main__":
    app.run()
