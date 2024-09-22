import pytest

from model.creature import Creature


@pytest.fixture
def creature():
    data = {
        'name': 'hunter',
        'hp': 10,
        'max_hp': 10
    }
    return Creature(**data)


def test_hp_limit(creature):
    creature.hp = creature.max_hp + 1
    assert creature.hp == creature.max_hp


def test_aliveness(creature):
    assert creature.is_alive is True
    creature.hp = -1
    assert creature.is_alive is False
    assert creature.hp == 0

    # Revive!
    creature.hp = 10
    creature.is_alive = True
    creature.hp = 0
    assert creature.is_alive is False
