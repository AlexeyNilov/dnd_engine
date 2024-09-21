from model.creature import create_creature
from model.object import TreeFood


data = {
    'name': 'The first oak',
    'hp': 100,
    'max_hp': 500
}
tree = create_creature(data)
print(tree)

data = {
    'name': 'The tree food',
    'value': 10
}
tree_food = TreeFood(**data)
print(tree_food)
