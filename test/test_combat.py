import pytest

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.creature import Creature
from dnd_engine.model.team import Team


@pytest.fixture
def team_red():
    return Team(name="Red", members=[get_creature("Wolf"), get_creature("Wolf")])


@pytest.fixture
def team_blue():
    return Team(name="Blue", members=[get_creature("Pig"), get_creature("Pig")])


@pytest.fixture
def combat(team_red, team_blue):
    return Combat(name="Test", teams=[team_red, team_blue], owner="Test")


def test_is_the_end(combat):
    assert combat.is_completed() is False
    combat.teams[0].is_loser = True
    assert combat.is_completed()


def test_is_the_end_no_alive_members(combat):
    assert combat.is_completed() is False
    for m in combat.teams[0].members:
        m.is_alive = False
    assert combat.is_completed()


def test_form_combat_queue(combat):
    combat.form_combat_queue()
    assert isinstance(combat.queue, list)
    assert len(combat.queue) == 4
    assert isinstance(combat.queue[0], Creature)
    combat.form_combat_queue()
    assert len(combat.queue) == 4


def test_get_target_for(combat, team_red, team_blue):
    assert combat.get_target_for(attacker=team_red.members[0]) == team_blue.members[0]


def test_advice(combat):
    r = combat.advice(combat.teams[0].members[0], combat.teams[1].members[1])
    assert r == [combat.teams[0].members[0].skills["bite"]] * 1


def test_get_team(combat):
    assert combat.get_team(combat.teams[0].members[0]).name == "Red"


def test_opposite_get_team(combat):
    assert combat.get_opposite_team(combat.teams[0].members[0]).name == "Blue"
