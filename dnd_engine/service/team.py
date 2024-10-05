from random import randint
from typing import List

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.team import Team


def generate_teams(size: int = 4) -> List[Team]:
    # Team Red
    wolfs = [get_creature("Wolf") for _ in range(randint(1, size))]
    red = Team(name="Team Red", members=wolfs)

    # Team Blue
    pigs = [get_creature("Pig") for _ in range(randint(1, size))]
    blue = Team(name="Team Blue", members=pigs)

    return [red, blue]
