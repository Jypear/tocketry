from tocketry import Tocketry
from tocketry.conds import scheduler_running

app = Tocketry(config={"shut_cond": scheduler_running(more_than="5 minutes")})
