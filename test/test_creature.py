import pytest

from data.logger import set_logging
from model.creature import Creature
from model.skill import Skill
from model.skill import SkillTypeNotFound
from model.skill_library import Consume


set_logging()


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


def test_apply_base_skill(creature):
    creature.skills['test'] = Skill()
    with pytest.raises(SkillTypeNotFound):
        creature.apply(skill=creature.skills['test'], to=creature)


def test_consume_self(creature):
    hp = creature.hp
    creature.skills['test'] = Consume()
    creature.compatible_with.append(creature.nature)
    assert creature.apply(skill=creature.skills['test'], to=creature) is False
    assert creature.hp == hp
