import random


def roll_xdy(x, y, modifier=0):
    return sum(random.randint(1, y) for _ in range(x)) + modifier


def roll_1d6(modifier: int = 0) -> int:
    return roll_xdy(1, 6, modifier)
