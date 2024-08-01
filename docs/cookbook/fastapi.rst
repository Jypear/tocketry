
Integrate FastAPI
=================

The simplest way to combine FastAPI app with Tocketry app 
is to start both as async tasks. You can modify the Tocketry's
runtime session in FastAPI. There is an existing example project:
`Tocketry with FastAPI (and React) <https://github.com/Jypear/tocketry-with-fastapi>`_

First, we create a simple Tocketry app
(let's call this ``scheduler.py``):

.. code-block:: python

    # Create Tocketry app
    from tocketry import Tocketry
    app = Tocketry(execution="async")


    # Create some tasks

    @app.task('every 5 seconds')
    async def do_things():
        ...

    if __name__ == "__main__":
        app.run()

Then we create a FastAPI app and manipulate the Tocketry
app in it (let's call this ``api.py``):

.. code-block:: python

    # Create FastAPI app
    from fastapi import FastAPI
    app = FastAPI()

    # Import the Tocketry app
    from scheduler import app as app_tocketry
    session = app_tocketry.session

    @app.get("/my-route")
    async def get_tasks():
        return session.tasks

    @app.post("/my-route")
    async def manipulate_session():
        for task in session.tasks:
            ...

    if __name__ == "__main__":
        app.run()

Then we combine these in one module
(let's call this ``main.py``):

.. code-block:: python

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

Note that we need to subclass the ``uvicorn.Server`` in order 
to make sure the scheduler is also closed when the FastAPI app
closes. Otherwise the system might not respond on keyboard interrupt.
