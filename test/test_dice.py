from dnd_engine.model import dice


def test_dice_1d6():
    assert 1 <= dice.roll_1d6() <= 6
