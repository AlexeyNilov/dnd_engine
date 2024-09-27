from collections import deque
from queue import Queue
from typing import Callable

from pydantic import BaseModel

from dnd_engine.model.creature import Creature

MAIN_QUEUE: Queue = Queue(1)
ACCEPT_EVENTS = False
END = object()


class Event(BaseModel):
    creature: Creature
    msg: str


EVENTS = deque([])


def publish_deque(creature: Creature, msg: str) -> None:
    EVENTS.append(Event(creature=creature, msg=msg))


def read_deque(func: Callable) -> None:
    while True:
        try:
            func(EVENTS.popleft())
        except IndexError:
            break
