from threading import Lock

from pydantic import Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated


GEZeroInt = Annotated[int, Field(ge=0)]
ConstrainedStr = Annotated[str, StringConstraints(min_length=1, to_lower=True, strip_whitespace=True)]


class LockList(list):
    def __init__(self, *args):
        super().__init__(*args)
        self._lock = Lock()  # Initialize a Lock for thread safety

    # Thread-safe append
    def append(self, item):
        with self._lock:
            super().append(item)

    # Thread-safe remove
    def remove(self, item):
        with self._lock:
            super().remove(item)

    # Thread-safe pop
    def pop(self, index=-1):
        with self._lock:
            return super().pop(index)

    # Thread-safe extending list
    def extend(self, iterable):
        with self._lock:
            super().extend(iterable)

    # Thread-safe insert
    def insert(self, index, item):
        with self._lock:
            super().insert(index, item)

    # You can also override other list operations like __getitem__, __setitem__, etc., if needed.

    # Optional: Thread-safe __getitem__
    def __getitem__(self, index):
        with self._lock:
            return super().__getitem__(index)

    # Optional: Thread-safe __setitem__
    def __setitem__(self, index, value):
        with self._lock:
            super().__setitem__(index, value)

    # Optional: Thread-safe __delitem__
    def __delitem__(self, index):
        with self._lock:
            super().__delitem__(index)
