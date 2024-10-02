from typing import List

from dnd_engine.data.bestiary import get_creature
from dnd_engine.data.db_dataclasses import Combats
from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_loader import save_combat_view
from dnd_engine.data.fastlite_loader import save_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import publish_deque
from dnd_engine.model.team import Team


def generate_teams() -> List[Team]:
    # Team Red
    wolfs = [get_creature("Wolf") for _ in range(4)]
    for wolf in wolfs:
        save_creature(wolf)
    red = Team(name="Team Red", members=wolfs, events_publisher=publish_deque)

    # Team Blue
    pigs = [get_creature("Pig") for _ in range(4)]
    blue = Team(name="Team Blue", members=pigs, events_publisher=publish_deque)
    for pig in pigs:
        save_creature(pig)

    return [red, blue]


# Combat
combats_table = DB.t.combats
combats_table.dataclass()
combats_table.xtra(owner="Arena")

# TODO Cycle it
combat_views = combats_table(limit=1)
if combat_views:
    cv: Combats = combat_views[0]
    if cv.status == "Not started":
        combat = Combat(
            name=cv.name,
            events_publisher=publish_deque,
            teams=generate_teams(),
            owner=cv.owner,
            round=cv.round,
            status=cv.status,
        )
        combat.form_combat_queue()
        combat.status = "Started"
        save_combat_view(combat)
