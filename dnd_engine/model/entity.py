from threading import Lock
from typing import ClassVar

from pydantic import BaseModel

from dnd_engine.model.shared import ConstrainedStr


class Entity(BaseModel):
    """See doc/entity.md for details"""

    id: str  # Must be uniq globally
    name: str
    nature: ConstrainedStr = "unknown"

    # Generate unique ID
    _id_counter: ClassVar[int] = 0
    _lock: ClassVar[Lock] = Lock()

    def __init__(self, **data):
        if "id" not in data.keys() or data["id"] is None:
            with self._lock:
                data["id"] = f"{self.__class__.__name__}_{self._get_next_id()}"
        super().__init__(**data)

    def _get_next_id(self) -> int:
        self.__class__._id_counter += 1
        return self.__class__._id_counter
