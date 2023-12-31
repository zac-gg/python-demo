import time

import reactivex
from reactivex import operators as ops


def failing(x):
    x = int(x)
    if not x % 2:
        raise Exception("Error")
    return x


def main():
    xs = reactivex.from_marbles("1-2-3-4-5-6-7-9-|").pipe(ops.publish())
    xs.pipe(ops.map(failing), ops.retry()).subscribe(print)

    xs.connect()  # Must connect. Cannot use ref_count() with publish()

    time.sleep(5)


if __name__ == "__main__":
    main()
