from components.ai import BlindEnemy, ConfusedEnemy, HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from game.entity import Actor, Item
# PC
player = Actor(
    char="@", 
    color=(255, 255, 255), 
    name="Player", 
    ai_cls=HostileEnemy, # It is overriden, do not worry
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_defense=10, base_power=15),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200)
    )
#Enemies
mouse = Actor(
    char="m", 
    color=(63, 127, 63), 
    name="Mouse",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=0, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20)
    )
rat = Actor(
    char="r", 
    color=(63, 127, 63), 
    name="Rat",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=1, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=40)
    )
bat = Actor(
    char="b", 
    color=(63, 127, 63), 
    name="Bat",
    ai_cls=BlindEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=50)
    )
giant_rat = Actor(
    char="g", 
    color=(63, 127, 63), 
    name="Giant Rat",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=5, base_defense=2, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100)
    )
the_rat_catcher = Actor(
    char="K", 
    color=(63, 127, 63), 
    name="The Rat Catcher",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=2, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0)
    )
# Items
# Consumables
pretzel = Item(
    char="!",
    color=(127, 0, 255),
    name="Pretzel",
    consumable=consumable.HealingConsumable(amount=4),
)
rock = Item(
    char=".",
    color=(255, 255, 0),
    name="Rock",
    consumable=consumable.RangedDamageConsumable(damage=2, maximum_range=5),
)
carrot_flute = Item(
    char="~",
    color=(207, 63, 255),
    name="Carrot Flute",
    consumable=consumable.ConfusionConsumable(number_of_turns=5)
)
firebomb = Item(
    char=".",
    color=(255, 0, 0),
    name="Firebomb",
    consumable=consumable.FirebombDamageConsumable(damage=12, radius=3)
)
# Equipment
# Equipment - weapons
wooden_stick = Item(
    char="/",
    color=(101, 67, 33),
    name="Wooden Stick",
    equippable=equippable.WoodenStick()
)
sword = Item(
    char="/",
    color=(192, 192, 192),
    name="Sword",
    equippable=equippable.Sword()
)
# Equipment - armor
leather_armor = Item(
    char="[",
    color=(101, 67, 33),
    name="Leather Armor",
    equippable=equippable.LeatherArmor()
)
chain_mail = Item(
    char="[",
    color=(192, 192, 192),
    name="Leather Armor",
    equippable=equippable.ChainMail()
)