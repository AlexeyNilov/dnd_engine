from dnd_engine.data.bestiary import get_creature
from dnd_engine.data.bestiary import get_skills
from dnd_engine.model.creature import Creature
from dnd_engine.model.skill_library import Attack


def test_get_creature():
    c = get_creature("Wolf")
    assert isinstance(c, Creature)
    c = get_creature("Wolf")
    assert isinstance(c, Creature)


def test_get_skills():
    data = {"bite": {"type": "Attack", "base": 2}}
    s = get_skills(data)
    assert isinstance(s["bite"], Attack)
    assert s["bite"].base == 2
