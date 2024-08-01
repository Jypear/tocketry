from tocketry import Tocketry
from tocketry.conds import scheduler_cycles

app = Tocketry(config={"shut_cond": scheduler_cycles(more_than=1)})
