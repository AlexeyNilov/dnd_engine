from collections import deque
from typing import Any
from typing import Callable
from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    source: str
    msg: str
    entity: Optional[Any] = None


EVENTS = deque[Event]()


def create_deque() -> deque:
    return deque[Event]()


def publish_to_deque(
    source: str,
    msg: str,
    entity: Optional[Any] = None,
    dq: deque = EVENTS,
) -> None:
    dq.append(Event(source=source, msg=msg, entity=entity))


def exec_on_deque(func: Callable, dq: deque = EVENTS) -> list:
    results = []
    while True:
        try:
            results.append(func(dq.popleft()))
        except IndexError:
            break
    return results


def print_deque(dq: deque = EVENTS) -> None:

    def print_event(e: Event):
        print(f"{e.source}: {e.msg}")

    exec_on_deque(print_event, dq=dq)


def get_deque(dq: deque = EVENTS) -> list:

    def get_event(e: Event):
        return f"{e.source}: {e.msg}"

    return exec_on_deque(get_event, dq=dq)
