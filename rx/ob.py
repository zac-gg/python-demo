
import random
import multiprocessing
import time


from reactivex import operators as ops, of, range, just, interval, scheduler


thread_count = multiprocessing.cpu_count()

thread_pool_scheduler = scheduler.ThreadPoolScheduler(thread_count)


def adding_delay(v):
    time.sleep(1)
    return v


takeFourNumbers = interval(0.1).pipe(

    ops.map(lambda a: adding_delay(a)),
    ops.subscribe_on(thread_pool_scheduler)

)


takeFourNumbers.subscribe(
    on_next=lambda s: print("From Task 1: {0}".format(s))
)


input("Press any key to exit\n")
