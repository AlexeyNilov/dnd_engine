# What is the simplest creature?

*See model/creature.py for the current implementation*

# Name and ID
A creature must have a name, right? Human names are not uniq but we probably want to distinguish creatures.
ID solves that. Name is something human readable, ID is an uniq string.

# Aliveness
What is the difference between being created and being alive?
A creature must be alive. Otherwise it is just a thing or an object.

What does it mean to be alive? Are undeads alive? I guess so.
Being alive gives possibility to become dead(is_alive=False).
HP(health point) is a measure of aliveness. When amount of HP becomes < 1 creature dies.

Being dead means a creature can't initiate any action on its own, but it can be used by other creatures.

# Growth
Being alive gives possibility to grow!

It feels like HP must have an upper limit. Is it so? If so, growth is the expansion of this limit.
Very often levels are used as a measure of growth. I'm not sure we need them.

To grow a creature must consume something(food, energy, knowledge, etc).

# Skills

*See model/skill.py for the current implementation*

To do anything a creature must know how to do it, to have a skill.
