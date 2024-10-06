# Entity (object)

*Refer to model/entity.py for the current implementation*

In reality, there are no "objects" as we typically think of them—just countless small elements like atoms, which behave according to the laws of physics. However, in computation-based simulations, we need to create objects, as programming languages and software do not allow us to manipulate individual atoms.

Domain-Driven Design (DDD) introduces the concept of entities, which represent these objects within the software domain. Unlike traditional objects that are often defined solely by their attributes, entities are primarily characterized by their unique identity.

## Naming

To be distinguishable, an entity must have a unique ID. To ensure this uniqueness, IDs are generated automatically. Additionally, a name property is provided to allow users to assign meaningful names to entities.

## Nature (Dao?) - Rejected for now

In reality, we are bound by many limitations — laws, ethics, and so on. To replicate similar constraints in a simulation, we need something. I'm not entirely sure what to call it, but for now, I’ll refer to it as the "nature of things" or Dao.

This concept is used to check compatibility between skills and entities.

## Skills

For a creature to perform any action, it must know how to do it — this is where skills come into play.

*See doc/skill.md for more details*

Action points = number of skills
