from data.logger import set_logging
from model.creature import Creature
from model.object import Resource
from model.skill import Consume


set_logging()
data = {
    'name': 'The first oak',
    'hp': 400,
    'max_hp': 500,
    'skills': {
        'drain': Consume()
    }
}
tree = Creature(**data)
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
