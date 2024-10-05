import pytest

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.team import Team


@pytest.fixture
def team():
    return Team(name="Red", members=[get_creature("Wolf"), get_creature("Pig")])
