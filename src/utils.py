import asyncio


def func(callback):
    asyncio.create_task(act(callback))

async def act(callback):
    print("Hello")
    await asyncio.sleep(1)
    print("World")
    callback()