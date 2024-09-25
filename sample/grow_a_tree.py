from typing import List

from data.logger import set_logging
from data.storage import get_creature
from dnd_engine.model.resource import Resource


set_logging()
tree = get_creature(name="The first oak")
tree.hp = tree.max_hp - 10
data = {"name": "Water", "value": 100, "nature": "water"}
water = Resource(**data)

fruit_data = {"name": "Fruit", "value": 50, "nature": "organic"}
fruits: List[Resource] = list()

while water.value > 0:
    tree.hp -= 1
    tree.apply(skill=tree.skills["eat"], to=water)
    if tree.hp == tree.max_hp:
        fruits.append(Resource(**fruit_data))
        tree.hp -= fruits[-1].value
        print("New fruit created")
    print(tree.model_dump(include={"name", "hp"}))

print(len(fruits))
print(tree.model_dump(include={"name", "hp", "max_hp", "is_alive", "skills"}))
