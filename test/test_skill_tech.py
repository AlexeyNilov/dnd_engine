import pytest

from dnd_engine.model.skill_library import Consume
from dnd_engine.model.skill_tech import get_skills_from_book
from dnd_engine.model.skill_tech import SkillRecord


@pytest.fixture
def skill_book():
    return [SkillRecord(name="eat", skill_class="Consume")]


def test_get_skills_from_book(skill_book):
    assert get_skills_from_book(skill_book) == {"eat": Consume(used=0, level=1, rate=1)}
