import pytest

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.team import Team

# from dnd_engine.service.battle import advice


@pytest.fixture
def team_red():
    return Team(name="Red", members=[get_creature("Wolf"), get_creature("Wolf")])


@pytest.fixture
def team_blue():
    return Team(name="Blue", members=[get_creature("Pig"), get_creature("Pig")])


@pytest.fixture
def combat(team_red, team_blue):
    return Combat(name="Test", teams=[team_red, team_blue], owner="Test")


# def test_advice(combat):
#     r = advice(combat, combat.teams[0].members[0])
#     assert r == [
#         (combat.teams[0].members[0].skills["bite"], combat.teams[1].members[0])
#     ]
