import pytest

from model.resource import Resource
from model.skill import calculate_level
from model.skill import Consume
from model.skill import Skill


@pytest.fixture
def food():
    data = {
        'name': 'food',
        'value': 10,
    }
    return Resource(**data)


@pytest.fixture
def skill():
    return Skill()


@pytest.fixture
def consume():
    return Consume()


def test_calculate_level():
    assert calculate_level(500) == 9
    assert calculate_level(0) == 1


def test_skill_level_up(skill):
    assert skill.level == 1
    skill.used = 10
    assert skill.level == 2


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
