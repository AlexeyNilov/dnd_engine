# Creature aka Body

*Refer to model/creature.py for the current implementation*

The Creature class inherits from the Entity class. The key difference is that creatures can be alive.

## Aliveness

What does it mean to be alive? Are undead beings alive? I suppose so.
Being alive means a creature has the potential to become dead (is_alive=False).
Health Points serve as a measure of aliveness. When HP drops below 1, the creature dies.

When a creature is dead, it cannot initiate any actions on its own, but it can still be used by other creatures.

## Growth

Being alive also means the ability to grow!

It seems logical that HP should have an upper limit. If that’s the case, growth refers to the expansion of this limit.
Often, levels are used as a measure of growth, although I'm not sure if we need them.

To grow, a creature must consume something—whether it's food, energy, knowledge, or something else.

## Survival

Constant/regular HP loss
Consuming resources

## Skills

For a creature to perform any action, it must know how to do it — this is where skills come into play.

*See doc/skill.md for more details*

Action points = number of skills

## Control

So far a creature doesn't have mind or will.
Battle spirits merge with creatures and control them during a combat.
