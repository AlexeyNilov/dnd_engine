from time import sleep
from typing import List

from dnd_engine.data.fastlite_dataclasses import Combats
from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_db import recreate_db
from dnd_engine.data.fastlite_loader import save_event_related_entity
from dnd_engine.model.combat import Combat
from dnd_engine.model.combat import Creature
from dnd_engine.model.command import Command
from dnd_engine.service.team import generate_teams
from dnd_engine.service.team import prepare_teams


recreate_db()
combats_table = DB.t.combats
combats_table.dataclass()
combats_table.xtra(owner="Arena")

while True:
    combat_views = combats_table(limit=1)

    if not combat_views:
        sleep(2)
        continue

    cv: Combats = combat_views[0]
    print(cv)

    if cv.status == "Not started":

        def get_input(creature: Creature) -> List[Command]:
            actions = list()
            target = combat.get_target_for(creature)
            actions.append(Command(skill_class="Attack", target=target))
            return actions

        combat = Combat(
            name=cv.name,
            events_publisher=save_event_related_entity,
            teams=generate_teams(size=1),
            owner=cv.owner,
            round=cv.round,
            status=cv.status,
        )

        prepare_teams(
            combat.teams,
            event_publisher=save_event_related_entity,
            get_commands=get_input,
        )

        combat.start()
