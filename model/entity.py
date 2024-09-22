from threading import Lock
from typing import ClassVar

from pydantic import BaseModel


class Entity(BaseModel):
    """ See doc/entity.md for details"""

    id: str  # Must be uniq globally
    name: str
    nature: str = 'unknown'

    # The following code is needed to automatic unique ID generation
    _id_counter: ClassVar[int] = 0
    _lock: ClassVar[Lock] = Lock()

    def __init__(self, **data):
        with self._lock:
            data['id'] = f'{self.__class__.__name__}_{self._get_next_id()}'
        super().__init__(**data)

    def _get_next_id(self) -> int:
        self.__class__._id_counter += 1
        return self.__class__._id_counter
