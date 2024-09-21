# What is the simplest creature?

See model/creature.py for the current implementation

# Name and ID
A creature must have a name, right? Human names are not uniq but we probably want to distinguish creatures.
ID solves that. Name is something human readable, ID is an uniq string.

# Alive
What is the difference between being created and being alive?
A creature must be alive. Otherwise it is just a thing or an object.

What does it mean to be alive? Are undeads alive? I guess so.
Being alive gives possibility to become dead.
HP is a measure of aliveness. When HP becomes < 1 creature dies (is_alive=False)
