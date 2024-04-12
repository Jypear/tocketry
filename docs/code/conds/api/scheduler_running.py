from tocketry import Rocketry
from tocketry.conds import scheduler_running

app = Rocketry(config={
    "shut_cond": scheduler_running(more_than="5 minutes")
})
