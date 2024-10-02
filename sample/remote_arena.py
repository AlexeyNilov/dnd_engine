# from dnd_engine.data.bestiary import get_creature
# from dnd_engine.data.fastlite_loader import save_combat_view
# from dnd_engine.data.fastlite_loader import save_creature
# from dnd_engine.model.combat import Combat
# from dnd_engine.model.event import publish_deque
# from dnd_engine.model.team import Team
from dnd_engine.data.fastlite_db import DB


# Team Red
# wolfs = [get_creature("Wolf") for _ in range(4)]
# for wolf in wolfs:
#     save_creature(wolf)
# red = Team(name="Team Red", members=wolfs, events_publisher=publish_deque)

# # Team Blue
# pigs = [get_creature("Pig") for _ in range(4)]
# blue = Team(name="Team Blue", members=pigs, events_publisher=publish_deque)
# for pig in pigs:
#     save_creature(pig)

# Combat
combats_table = DB.t.combats
combats_table.dataclass()
combat_view = combats_table["Arena_1"]
print(combat_view)
