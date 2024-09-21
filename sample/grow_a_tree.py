from data.logger import set_logging
from data.storage import get_creature
from model.object import Resource


set_logging()
tree = get_creature(name='The first oak')
print(tree)

data = {
    'name': 'Water',
    'value': 10,
    'core': 'water'
}
water = Resource(**data)
print(water)

while water.value > 0:
    tree.apply(what=tree.skills['drain'], to=water)

print(tree)
