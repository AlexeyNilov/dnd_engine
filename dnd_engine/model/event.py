from collections import deque
from typing import Any
from typing import Callable

from pydantic import BaseModel


class Event(BaseModel):
    source: Any
    msg: str


EVENTS = deque[Event]()


def publish_deque(source: Any, msg: str) -> None:
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
