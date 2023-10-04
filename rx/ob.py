
import random
import multiprocessing
import time
from reactivex import operators as ops, of, range, interval, scheduler, create, just, from_future, merge, Observable
from reactivex.scheduler.eventloop import AsyncIOScheduler
from reactivex.subject import Subject
import asyncio
from futu import getUSD2THBRate
from p2p import getP2PRate
import aiohttp


async def batchFetch(v):
    async with aiohttp.ClientSession() as session:
        rate_futu, rate_p2p = await asyncio.gather(
            getUSD2THBRate(session),
            getP2PRate(session),
        )
        return rate_futu, rate_p2p


def asyncFN(observer, scheduler):
    loop = asyncio.get_event_loop()
    price = loop.run_until_complete(batchFetch())
    loop.close()
    observer.on_next(price)


async def fetch_api(data):
    await asyncio.sleep(0.3)  # Simulating network latency
    return f"Response for {data}"


async def foo():
    res = await batchFetch(1)
    return res


def intervalRead(rate, fun) -> Observable:
    loop = asyncio.get_event_loop()
    return interval(rate).pipe(
        ops.map(lambda i: from_future(loop.create_task(fun()))),
        ops.merge_all()
    )


async def main(loop):
    obs = intervalRead(1, foo)
    obs.subscribe(
        on_next=lambda item: print(item),
        scheduler=AsyncIOScheduler(loop)
    )

loop = asyncio.get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
