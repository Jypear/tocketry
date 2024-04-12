from tocketry import Rocketry
from tocketry.conds import scheduler_cycles

app = Rocketry(config={
    "shut_cond": scheduler_cycles(more_than=1)
})
