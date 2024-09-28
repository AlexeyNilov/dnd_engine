import pytest

from dnd_engine.model.creature import Creature
from dnd_engine.model.resource import Resource
from dnd_engine.model.skill_library import Consume


@pytest.fixture
def food():
    data = {
        "name": "food",
        "value": 10,
        "nature": "organic"
    }
    return Resource(**data)


@pytest.fixture
def creature():
    data = {"name": "hunter", "hp": 9, "max_hp": 10}
    c = Creature(**data)
    c.compatible_with.append("organic")
    return c


@pytest.fixture
def consume():
    return Consume()


def test_consume_skill(food, consume, creature):
    gain = consume.use(who=creature, to=food)
    assert gain == 1
    assert food.value == 9
    assert consume.used == 1


def test_consume_empty_resource(food, consume, creature):
    food.value = 0
    gain = consume.use(who=creature, to=food)
    assert gain == 0


def test_consume_when_value_less_then_rate(food, consume, creature):
    food.value = 1
    consume.base_rate = 2
    gain = consume.use(who=creature, to=food)
    assert gain == 1


def test_consume_rate_increase(food, consume, creature):
    consume.level = 2
    assert consume.use(who=creature, to=food) == 2
