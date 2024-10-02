from typing import Callable
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated


ZeroPositiveInt = Annotated[int, Field(ge=0)]
ConstrainedStr = Annotated[
    str, StringConstraints(min_length=1, to_lower=True, strip_whitespace=True)
]


class EventModel(BaseModel):
    name: str
    events_publisher: Optional[Callable] = None

    def publish_event(self, msg: str):
        if callable(self.events_publisher):
            self.events_publisher(self.name, msg)
