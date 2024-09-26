from queue import Queue
from threading import Thread
from typing import Callable

from pydantic import BaseModel

from dnd_engine.model.entity import Entity

MAIN_QUEUE: Queue = Queue(1)
END = object()


class Event(BaseModel):
    entity: Entity
    msg: str


def publish_event(entity: Entity, msg: str, q: Queue = MAIN_QUEUE, timeout: int = 5) -> None:
    q.put(Event(entity=entity, msg=msg), timeout=timeout)


def get_event(q: Queue = MAIN_QUEUE, timeout: int = 5) -> Event:
    return q.get(timeout=timeout)


def stop(q: Queue = MAIN_QUEUE):
    q.put(END)


def event_manager(func: Callable, q: Queue = MAIN_QUEUE):
    while True:
        event = get_event(q=q)
        if event == END:
            return

        func(event)

        q.task_done()


def start_event_manager(func: Callable, q: Queue = MAIN_QUEUE) -> Thread:
    thread = Thread(target=event_manager, args=(func, q))
    thread.start()
    return thread


def stop_event_manager(thread: Thread, q: Queue = MAIN_QUEUE):
    stop(q=q)
    thread.join()
