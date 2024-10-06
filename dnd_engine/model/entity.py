from threading import Lock
from typing import ClassVar

from dnd_engine.model.shared import EventModel


ID_COUNTER = 0


class Entity(EventModel):
    """See doc/entity.md for details"""

    id: int  # Must be uniq globally

    _id_counter: ClassVar[int] = 0
    _lock: ClassVar[Lock] = Lock()

    def __init__(self, **data):
        if "id" not in data.keys() or data["id"] is None:
            with self._lock:
                data["id"] = self._get_next_id()
        super().__init__(**data)

    def _get_next_id(self) -> int:
        global ID_COUNTER
        ID_COUNTER += 1
        return ID_COUNTER

    def publish_event(self, msg: str):
        if callable(self.events_publisher):
            self.events_publisher(f"{self.name}_{self.id}", msg, self)
