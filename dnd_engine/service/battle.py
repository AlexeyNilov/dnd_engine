from random import randint
from typing import List

from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.team import Team


def generate_teams(size: int = 4) -> List[Team]:
    # Team Red
    wolfs = [get_creature("Wolf") for _ in range(randint(1, size))]
    red = Team(name="Team Red", members=wolfs)

    # Team Blue
    pigs = [get_creature("Pig") for _ in range(randint(1, size))]
    blue = Team(name="Team Blue", members=pigs)

    return [red, blue]


# class AdviceNotFound(Exception):
#     pass


# def advice_hp_based(
#     combat: Combat, myself: Creature, ap: int
# ) -> List[Tuple[Skill, Creature]]:
#     target = combat.get_target_for(myself)
#     hp_left = int(round(100 * myself.hp / myself.max_hp, 0))
#     actions = list()
#     if hp_left < 50:
#         actions.append((myself.get_skill_by_class("Move"), target))
#     else:
#         actions.append((myself.get_skill_by_class("Attack"), target))
#     for _ in range(1, ap):
#         actions.append((myself.get_skill_by_class("Attack"), target))
#     return actions


# def advice_random(
#     combat: Combat, myself: Creature, ap: int
# ) -> List[Tuple[Skill, Creature]]:
#     target = combat.get_target_for(myself)
#     actions = list()
#     for _ in range(ap):
#         skill_name = str(random.choice(list(myself.skills.keys())))
#         actions.append((myself.skills[skill_name], target))
#     return actions


# def advice(
#     combat: Combat, myself: Creature, level: int = 1, input_getter: Callable = None
# ) -> List[Tuple[Skill, Creature]]:
#     if isinstance(input_getter, Callable) and myself in combat.teams[0].members:
#         return input_getter(combat, myself)

#     # max_ap = myself.get_action_points()
#     max_ap = 1

#     if level == 0:  # Random choice
#         return advice_random(combat, myself, max_ap)

#     if level == 1:  # HP based choice
#         return advice_hp_based(combat, myself, max_ap)

#     raise AdviceNotFound


def next_round(combat: Combat):
    combat.round += 1
    combat.publish_event(f"Round {combat.round}")

    for creature in combat.queue:
        if combat.is_completed():
            break
        if not creature.is_alive:
            continue

        creature.act()
