from dnd_engine.data import fastite_loader as fl_loader
from dnd_engine.data.bestiary import get_creature


fl_loader.recreate_db()
fl_loader.save_creature(get_creature("Wolf"))
fl_loader.save_creature(get_creature("Pig"))
fl_loader.save_creature(get_creature("Oak"))


for c in fl_loader.DB.t.creatures():
    print(c)

for s in fl_loader.DB.t.skill_records():
    print(s)
