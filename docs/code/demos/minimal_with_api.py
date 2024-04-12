from tocketry import Rocketry
from tocketry.conds import daily

app = Rocketry()

@app.task(daily)
def do_things():
    ...

if __name__ == "__main__":
    app.run()
