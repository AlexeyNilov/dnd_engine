from dnd_engine.data.fastlite_loader import load_creature
from dnd_engine.model.command import Command
from dnd_engine.model.creature import Creature
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque


cr = load_creature(id=1)


def generate_command(creature: Creature):
    c = Command(skill_class="Attack", target=creature)
    return [c] * 5


cr.events_publisher = publish_deque
cr.get_commands = generate_command

for _ in range(2):
    print(cr.hp, cr.skills["bite"], cr.skills["dodge"], sep=" | ")
    cr.act()

print_deque()
