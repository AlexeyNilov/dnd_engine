import pytest

from model.skill import calculate_level
from model.skill import Skill


@pytest.fixture
def skill():
    return Skill()


def test_calculate_level():
    assert calculate_level(500) == 9
    assert calculate_level(0) == 1


def test_skill_level_up(skill):
    assert skill.level == 1
    skill.used = 10
    assert skill.level == 2
