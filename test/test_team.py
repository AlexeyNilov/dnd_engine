import pytest

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.team import Team


@pytest.fixture
def team():
    return Team(name="Red", members=[get_creature("Wolf"), get_creature("Pig")])


def test_remove_dead_members(team):
    for member in team.members:
        member.is_alive = False
    team.remove_dead_members()
    assert team.members == []
    assert team.is_loser
