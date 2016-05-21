import bs4

from typing import List
import asyncio


def foo(a: List[str]) -> int:
    return a


s = foo(["12"])
s.decode('12')


async def factorial():
    global taskid
    while 1:
        task = await father_child.get()
        # child_father.put(task)
        await asyncio.sleep(2)
        await child_father.put(task)


def genFure():
    future = asyncio.Future()
    future.set_result(100)
    # print(loop.create_task(asyncio.sleep(4)))
    # future.set_result(100)
    return future


def callback(*args):
    print("callback {}".format(str(args)))


async def wrapfuture():
    await asyncio.sleep(2)
    asyncio.ensure_future(main(), loop=loop)


async def main():
    for _ in range(10):
        print("father put task {} {}".format(_, type(_)))
        await father_child.put(_)
    tasks = [
        asyncio.ensure_future(factorial()),
        asyncio.ensure_future(factorial()),
        asyncio.ensure_future(factorial())]
    while 1:
        task = await child_father.get()
        print("father know {} finished".format(task))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    father_child = asyncio.Queue()
    child_father = asyncio.Queue()
    loop.run_until_complete(main())
    loop.run_forever()
