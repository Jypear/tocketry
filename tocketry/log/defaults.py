from tocketry.redbird.logging import RepoHandler
from tocketry.redbird.repos import MemoryRepo
from .log_record import MinimalRecord


def create_default_handler():
    "Create default handler that can be read"
    return RepoHandler(repo=MemoryRepo(model=MinimalRecord))
