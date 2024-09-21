from model.creature import Creature
from model.object import TreeFood
from model.skill import Consume


data = {
    'name': 'The first oak',
    'hp': 100,
    'max_hp': 500,
    'skills': [Consume()]
}
tree = Creature(**data)
print(tree)

data = {
    'name': 'The tree food',
    'value': 10
}
tree_food = TreeFood(**data)
print(tree_food)
