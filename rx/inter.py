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


async def main(loop):
    obs = interval(1).pipe(ops.take(4))
    obs.subscribe(
        on_next=lambda item: print(item),
        scheduler=AsyncIOScheduler(loop)
    )

loop = asyncio.get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
