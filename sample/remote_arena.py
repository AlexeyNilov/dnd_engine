from time import sleep
from typing import List
from typing import Tuple

from dnd_engine.data.fastlite_dataclasses import Combats
from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_loader import load_action
from dnd_engine.data.fastlite_loader import save_action
from dnd_engine.data.fastlite_loader import save_combat_view
from dnd_engine.data.fastlite_loader import save_creature
from dnd_engine.data.fastlite_loader import save_event
from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.event import Event
from dnd_engine.model.skill import Skill
from dnd_engine.service.battle import generate_teams
from dnd_engine.service.battle import next_round


combats_table = DB.t.combats
combats_table.dataclass()
combats_table.xtra(owner="Arena")


def publish_event(source: str, msg: str) -> None:
    print(f"{source}: {msg}")
    save_event(Event(source=source, msg=msg))


def save_team_members(combat: Combat):
    for team in combat.teams:
        for cr in team.members:
            save_creature(cr)


def get_remote_input(
    combat: Combat, creature: Creature
) -> List[Tuple[Skill, Creature]]:
    remote_input = list()
    target = combat.get_target_for(creature)
    action = save_action({"attacker_id": creature.id, "target_id": target.id})
    print(action)
    while True:
        sleep(1)
        action = load_action(id=action["id"])
        if action["skill_classes"]:
            break

    skill = creature.get_skill_by_class(action["skill_classes"])
    remote_input.append((skill, target))
    return remote_input


def cycle_rounds(combat: Combat):
    while not combat.is_completed():
        try:
            cv: Combats = combats_table[combat.name]
        except Exception:
            break

        if cv.status == "Started" and cv.round is not None and cv.round > combat.round:
            next_round(combat, input_getter=get_remote_input)
            cv.status = combat.status
            combats_table.upsert(cv)
            save_team_members(combat)

        sleep(1)


while True:
    combat_views = combats_table(limit=1)

    if not combat_views:
        sleep(2)
        continue

    cv: Combats = combat_views[0]
    print(cv)

    if cv.status == "Not started":
        combat = Combat(
            name=cv.name,
            events_publisher=publish_event,
            teams=generate_teams(events_publisher=publish_event),
            owner=cv.owner,
            round=cv.round,
            status=cv.status,
        )
        combat.form_combat_queue()
        save_combat_view(combat)
        save_team_members(combat)
        cycle_rounds(combat)
    else:
        sleep(5)
        combats_table.delete(cv.name)
