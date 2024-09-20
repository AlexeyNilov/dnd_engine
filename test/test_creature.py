import pytest

from model.creature import Creature


@pytest.fixture
def creature():
    data = {
        'id': '0',
        'name': 'hunter',
        'hp': 10,
        'max_hp': 10
    }
    return Creature(**data)


def test_hp_limit(creature):
    with pytest.raises(ValueError, match='hp must be less than max_hp'):
        creature.hp = creature.max_hp + 1
