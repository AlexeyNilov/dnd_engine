from data.logger import set_logging
from data.storage import get_creature
from model.resource import Resource


set_logging()
tree = get_creature(name='The first oak')
tree.hp = tree.max_hp - 10
data = {'name': 'Water', 'value': 100, 'nature': 'water'}
water = Resource(**data)

while water.value > 0:
    tree.hp -= 1
    tree.apply(skill=tree.skills['eat'], to=water)
    print(tree.model_dump(include={'name', 'hp'}))

print(tree.model_dump(include={'name', 'hp', 'max_hp', 'is_alive', 'skills'}))
