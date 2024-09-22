from data.logger import set_logging
from data.storage import get_creature
from model.resource import Resource


set_logging()
tree = get_creature(name='The first oak')

data = {
    'name': 'Water',
    'value': 20,
    'nature': 'water'
}
water = Resource(**data)

data = {
    'name': 'Food',
    'value': 10,
    'nature': 'organic'
}
food = Resource(**data)

while water.value > 0:
    tree.apply(what=tree.skills['eat'], to=water)
    tree.apply(what=tree.skills['eat'], to=food)

print(tree.model_dump(include={'name', 'hp', 'max_hp', 'is_alive', 'skills'}))
