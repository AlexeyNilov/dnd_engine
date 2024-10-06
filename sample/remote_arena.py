from time import sleep
from typing import List

from dnd_engine.data.fastlite_dataclasses import Combats
from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_loader import cleanup
from dnd_engine.data.fastlite_loader import clear_actions
from dnd_engine.data.fastlite_loader import get_action_by_attacker
from dnd_engine.data.fastlite_loader import save_event_related_entity
from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.command import Command
from dnd_engine.service.team import generate_teams
from dnd_engine.service.team import prepare_teams


combats_table = DB.t.combats
combats_table.dataclass()
combats_table.xtra(owner="Arena")
creatures_table = DB.t.creatures


def get_actions(creature: Creature, combat: Combat) -> List[Command]:
    target = combat.get_target_for(creature)
    if creature.name == "Wolf":
        for _ in range(200):
            sleep(0.1)

            try:
                action = get_action_by_attacker(attacker_id=creature.id)
            except Exception:
                continue

            clear_actions()
            skill_names = action["skill_names"].split(";")
            return [
                Command(skill_name=skill_name, target=target)
                for skill_name in skill_names
            ]

    return [Command(skill_name="bite", target=target)]


cleanup()
while True:
    print("Waiting for combat to start", end="\r")
    combat_views = combats_table(limit=1)

    if not combat_views:
        sleep(0.1)
        continue

    cv: Combats = combat_views[0]

    if cv.status != "Not started":
        sleep(0.1)
        continue

    combat = Combat(
        name=cv.name,
        events_publisher=save_event_related_entity,
        teams=generate_teams(size=5),
        owner=cv.owner,
        round=cv.round,
        status=cv.status,
    )

    def get_input(creature: Creature):
        return get_actions(creature, combat)

    prepare_teams(
        combat.teams,
        event_publisher=save_event_related_entity,
        get_commands=get_input,
    )

    print("\n\n\n\nStart new combat!")
    combat.start()
    sleep(1)
    cleanup()
