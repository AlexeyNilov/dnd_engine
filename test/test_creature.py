import pytest

from dnd_engine.data.logger import set_logging
from dnd_engine.model import creature as cr
from dnd_engine.model.command import Command
from dnd_engine.model.resource import Resource
from dnd_engine.model.skill import Skill
from dnd_engine.model.skill import SkillMethodNotImplemented
from dnd_engine.model.skill import SkillNotFound
from dnd_engine.model.skill_library import Attack
from dnd_engine.model.skill_library import Consume


set_logging()


@pytest.fixture
def creature() -> cr.Creature:
    data = {"name": "hunter", "hp": 9, "max_hp": 10}
    c = cr.Creature(**data)
    c.skills["eat"] = Consume()
    return c


@pytest.fixture
def attack_creature(creature) -> cr.Creature:
    creature.skills["bite"] = Attack()
    return creature


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
    creature.skills = {}
    creature.skills["test"] = Skill()
    with pytest.raises(SkillMethodNotImplemented):
        creature.apply(skill_name="test", to=creature)

    with pytest.raises(SkillNotFound):
        creature.apply(skill_name="eat", to=creature)


def test_use_consume_skill_on_self(creature):
    hp = creature.hp
    assert creature.apply("eat", to=creature) is False
    assert creature.hp == hp


def test_use_consume_skill(creature):
    hp = creature.hp
    food = Resource(name="food")
    value = food.value
    assert creature.apply("eat", to=food)
    assert creature.hp == hp + 1
    assert food.value == value - 1


def test_use_consume_skill_above_max_hp(creature):
    creature.hp = creature.max_hp
    food = Resource(name="food")
    value = food.value
    assert creature.apply("eat", to=food) is False
    assert food.value == value


def test_get_action_points(creature):
    assert creature.get_action_points() == 1


def test_act(attack_creature):

    def generate_command(attack_creature: cr.Creature):
        c = Command(skill_name="bite", target=attack_creature)
        return [c] * 5

    attack_creature.get_commands = generate_command
    attack_creature.act()
    assert attack_creature.hp == 7
