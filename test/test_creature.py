import pytest

from data.logger import set_logging
from model.creature import Creature
from model.creature import use_consume_skill
from model.resource import Resource
from model.skill import Skill
from model.skill import SkillTypeNotFound
from model.skill_library import Consume


set_logging()


@pytest.fixture
def creature():
    data = {
        'name': 'hunter',
        'hp': 9,
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


def test_use_consume_skill_on_self(creature):
    hp = creature.hp
    creature.compatible_with.append(creature.nature)
    assert use_consume_skill(creature=creature, skill=Consume(), to=creature) is False
    assert creature.hp == hp


def test_use_consume_skill(creature):
    hp = creature.hp
    food = Resource(name='food')
    value = food.value
    creature.compatible_with.append(food.nature)
    assert use_consume_skill(creature=creature, skill=Consume(), to=food)
    assert creature.hp == hp + 1
    assert food.value == value - 1


def test_use_consume_skill_above_max_hp(creature):
    creature.hp = creature.max_hp
    food = Resource(name='food')
    value = food.value
    creature.compatible_with.append(food.nature)
    assert use_consume_skill(creature=creature, skill=Consume(), to=food) is False
    assert food.value == value
