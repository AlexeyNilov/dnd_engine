from collections import deque
from typing import Callable

from pydantic import BaseModel

from dnd_engine.model.creature import Creature


class Event(BaseModel):
    creature: Creature
    msg: str


EVENTS = deque[Event]()


def publish_deque(creature: Creature, msg: str) -> None:
    EVENTS.append(Event(creature=creature, msg=msg))


def read_deque(func: Callable) -> None:
    while True:
        try:
            func(EVENTS.popleft())
        except IndexError:
            break
