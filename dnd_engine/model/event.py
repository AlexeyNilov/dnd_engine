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


def exec_on_deque(func: Callable) -> list:
    results = []
    while True:
        try:
            results.append(func(EVENTS.popleft()))
        except IndexError:
            break
    return results


def print_deque() -> None:

    def print_event(e: Event):
        print(f"{e.source.name}: {e.msg}")

    exec_on_deque(print_event)


def get_deque() -> list:

    def get_event(e: Event):
        return f"{e.source.name}: {e.msg}"

    return exec_on_deque(get_event)
