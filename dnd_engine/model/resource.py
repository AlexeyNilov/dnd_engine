from pydantic import PositiveInt

from dnd_engine.model.shared import EventModel


class Resource(EventModel):
    value: PositiveInt = 1
