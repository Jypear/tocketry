import asyncio
from tocketry import Tocketry

app = Tocketry(execution="async")


@app.task()
async def do_things(): ...


async def main():
    "Launch Tocketry app (and possibly something else)"
    tocketry_task = asyncio.create_task(app.serve())
    # Start possibly other async apps
    await tocketry_task


if __name__ == "__main__":
    asyncio.run(main())
