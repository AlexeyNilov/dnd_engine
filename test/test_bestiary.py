from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.creature import Creature


def test_get_creature():
    assert isinstance(get_creature("Wolf"), Creature)
