from model.creature import create_creature


data = {
    'name': 'The first oak',
    'hp': 100,
    'max_hp': 500
}
tree = create_creature(data)
print(tree)
