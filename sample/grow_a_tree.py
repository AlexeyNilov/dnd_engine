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

data = {
    'name': 'Food',
    'value': 10,
    'core': 'organic'
}
food = Resource(**data)
print(food)


while water.value > 0:
    tree.apply(what=tree.skills['drain'], to=water)
    tree.apply(what=tree.skills['drain'], to=food)

print(tree)
