from model.creature import Creature
from model.object import TreeFood


data = {
    'name': 'The first oak',
    'hp': 100,
    'max_hp': 500
}
tree = Creature(**data)
print(tree)

data = {
    'name': 'The tree food',
    'value': 10
}
tree_food = TreeFood(**data)
print(tree_food)
