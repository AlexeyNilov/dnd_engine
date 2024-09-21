from threading import Lock
from typing import ClassVar

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt
from typing_extensions import Annotated


GEZeroInt = Annotated[int, Field(ge=0)]


class ModelException(Exception):
    pass


class BaseObject(BaseModel):
    """ Simple object"""

    id: str  # Must be uniq globally
    name: str

    # Class-level variables for uniq id generation
    _id_counter: ClassVar[int] = 0
    _lock: ClassVar[Lock] = Lock()

    def __init__(self, **data):
        with self._lock:
            data['id'] = f'{self.__class__.__name__}_{self._get_next_id()}'
        super().__init__(**data)

    def _get_next_id(self) -> int:
        """Fetch and increment the global id."""
        self.__class__._id_counter += 1
        return self.__class__._id_counter


class Resource(BaseObject):
    value: PositiveInt = 1
    core: str
