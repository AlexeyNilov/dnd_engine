import pytest

from model.object import Food
from model.skill import ConsumeFood


@pytest.fixture
def food():
    data = {
        'name': 'The tree food',
        'value': 10
    }
    return Food(**data)


def test_consume_food_skill(food):
    skill = ConsumeFood()
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
