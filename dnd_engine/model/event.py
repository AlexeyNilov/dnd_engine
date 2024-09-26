from queue import Queue
from threading import Thread
from typing import Callable

from pydantic import BaseModel

from dnd_engine.model.creature import Creature

MAIN_QUEUE: Queue = Queue(1)
ACCEPT_EVENTS = False
END = object()


class Event(BaseModel):
    creature: Creature
    msg: str


def publish_event(creature: Creature, msg: str, q: Queue = MAIN_QUEUE, timeout: int = 5) -> None:
    if ACCEPT_EVENTS:
        q.put(Event(creature=creature, msg=msg), timeout=timeout)


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
    global ACCEPT_EVENTS
    ACCEPT_EVENTS = True
    thread = Thread(target=event_manager, args=(func, q))
    thread.start()
    return thread


def stop_event_manager(thread: Thread, q: Queue = MAIN_QUEUE):
    global ACCEPT_EVENTS
    ACCEPT_EVENTS = False
    stop(q=q)
    thread.join()
