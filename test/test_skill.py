import pytest

from model.resource import Resource
from model.skill import calculate_level
from model.skill import Consume


@pytest.fixture
def food():
    data = {
        'name': 'food',
        'value': 10,
    }
    return Resource(**data)


def test_calculate_level():
    assert calculate_level(500) == 9
    assert calculate_level(0) == 1


def test_consume_skill(food):
    skill = Consume()
    gain = skill.use(to=food)
    assert gain == 1
    assert food.value == 9
    assert skill.used == 1

    food.value = 0
    gain = skill.use(to=food)
    assert gain == 0

    food.value = 1
    skill.rate = 2
    gain = skill.use(to=food)
    assert gain == 1
