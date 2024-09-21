from data.logger import set_logging
from model.creature import Creature
from model.object import Food
from model.skill import ConsumeFood


set_logging()
data = {
    'name': 'The first oak',
    'hp': 400,
    'max_hp': 500,
    'skills': {
        'eat': ConsumeFood()
    }
}
tree = Creature(**data)
print(tree)

data = {
    'name': 'The tree food',
    'value': 10
}
food = Food(**data)
print(food)

while food.value > 0:
    tree.apply(what=tree.skills['eat'], to=food)

print(tree)
