import pytest

from model.object import Resource
from model.skill import Consume


@pytest.fixture
def food():
    data = {
        'name': 'food',
        'value': 10,
        'core': 'organic'
    }
    return Resource(**data)


def test_consume_food_skill(food):
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
