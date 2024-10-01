from dnd_engine.data import storage_fastlite as sf
from dnd_engine.data.bestiary import get_creature


sf.DB.t.creatures.drop()
sf.create_creatures_table()
sf.DB.t.skill_records.drop()
sf.create_skill_records_table()
sf.DB.t.events.drop()
sf.create_events_table()


sf.save_creature(get_creature("Wolf"))
sf.save_creature(get_creature("Pig"))
sf.save_creature(get_creature("Oak"))


for c in sf.DB.t.creatures():
    print(c)

for s in sf.DB.t.skill_records():
    print(s)
