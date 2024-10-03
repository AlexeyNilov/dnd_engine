from random import randint
from typing import Callable
from typing import List

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.team import Team


def generate_teams(events_publisher: Callable, size: int = 4) -> List[Team]:
    # Team Red
    wolfs = [
        get_creature("Wolf", events_publisher=events_publisher)
        for _ in range(randint(1, size))
    ]
    red = Team(name="Team Red", members=wolfs, events_publisher=events_publisher)

    # Team Blue
    pigs = [
        get_creature("Pig", events_publisher=events_publisher)
        for _ in range(randint(1, size))
    ]
    blue = Team(name="Team Blue", members=pigs, events_publisher=events_publisher)

    return [red, blue]
