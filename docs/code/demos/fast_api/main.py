import asyncio

import uvicorn

from api import app as app_fastapi
from scheduler import app as app_tocketry


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Tocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        app_tocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    "Run scheduler and the API"
    server = Server(config=uvicorn.Config(app_fastapi, workers=1, loop="asyncio"))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_tocketry.serve())

    await asyncio.wait([sched, api])


if __name__ == "__main__":
    asyncio.run(main())
