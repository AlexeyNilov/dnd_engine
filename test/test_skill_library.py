import pytest

from dnd_engine.model.resource import Resource
from dnd_engine.model.skill_library import Consume


@pytest.fixture
def food():
    data = {
        "name": "food",
        "value": 10,
    }
    return Resource(**data)


@pytest.fixture
def consume():
    return Consume()


def test_consume_skill(food, consume):
    gain = consume.use(to=food)
    assert gain == 1
    assert food.value == 9
    assert consume.used == 1


def test_consume_empty_resource(food, consume):
    food.value = 0
    gain = consume.use(to=food)
    assert gain == 0


def test_consume_when_value_less_then_rate(food, consume):
    food.value = 1
    consume.rate = 2
    gain = consume.use(to=food)
    assert gain == 1
