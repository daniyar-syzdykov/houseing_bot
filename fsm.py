import sys
import time 
import random
from threading import Thread
from enum import Enum, auto
import heapq
import types

def random_delay():
    return random.random() * 5

def random_countdown():
    return random.randrange(5)

@types.coroutine
def sleep(delay):
    yield Op.WAIT, delay



async def launch_rocket(delay, countdown):
    await sleep(delay)
    for i in reversed(range(countdown)):
        print(f'{i + 1}...')
        await sleep(1)
    print('Rocket Launch')

class State(Enum):
    WAITING = auto()
    COUNTING = auto()
    LAUNCHING = auto()

class Op(Enum):
    WAIT = auto()
    STOP = auto()

class Launch:
    def __init__(self, delay, countdown):
        self._delay = delay
        self._countdown = countdown
        self._state = State.WAITING
    def step(self):
        if self._state is State.WAITING:
            self._state = State.COUNTING
            return Op.WAIT, self._delay
        if self._state is State.COUNTING:
            if self._countdown == 0:
                self._state = State.LAUNCHING
            else:
                print(f'{self._countdown}...')
                self._countdown -=1
                return Op.WAIT, 1
        if self._state is State.LAUNCHING:
            print('Rcker Launched!')
            return Op.STOP, None
        assert False, self._state

def now():
    return time.time()

def run_fsm(rockets):
    start = now()
    work = [(start, i, launch_rocket(d, c)) for i, (d, c) in enumerate(rockets)]
    while work:
        step_at, id, launch = heapq.heappop(work)
        wait = step_at - now()
        if wait > 0:
            time.sleep(max(0, wait))
        try:
            op, arg = launch.send(None)
        except StopIteration:
            continue
        if op is Op.WAIT:
            step_at = arg + now() 
            heapq.heappush(work, (step_at, id, launch))
        else:
            assert False, op

def rockets():
    N = 10000
    return [(random_delay(), random_countdown()) for _ in range(N)]

def run_threads(rockets):
    threads = [Thread(target=launch_rocket, args=(d, c)) for d, c in rockets]
    for i in threads:
        i.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    run_fsm(rockets())
