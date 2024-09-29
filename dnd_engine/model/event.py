from collections import deque
from typing import Callable
from typing import Union

from pydantic import BaseModel

from dnd_engine.model.creature import Creature
from dnd_engine.model.team import Team


class Event(BaseModel):
    source: Union[Creature, Team]
    msg: str


EVENTS = deque[Event]()


def publish_deque(source: Union[Creature, Team], msg: str) -> None:
    EVENTS.append(Event(source=source, msg=msg))


def exec_on_deque(func: Callable) -> None:
    while True:
        try:
            func(EVENTS.popleft())
        except IndexError:
            break


def print_deque():

    def print_event(e: Event):
        print(f"{e.source.name}: {e.msg}")

    exec_on_deque(print_event)
