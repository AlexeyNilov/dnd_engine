import pytest

from model.creature import create_creature


@pytest.fixture
def creature():
    data = {
        'name': 'hunter',
        'hp': 10,
        'max_hp': 10
    }
    return create_creature(data)


def test_hp_limit(creature):
    creature.hp = creature.max_hp + 1
    assert creature.hp == creature.max_hp


def test_aliveness(creature):
    creature.hp = -1
    assert creature.is_alive is False
    assert creature.hp == 0
