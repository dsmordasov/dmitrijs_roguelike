from components.ai import BlindEnemy, ConfusedEnemy, HostileEnemy, BossEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from game.entity import Actor, Item
import game.color as color
# PC
player = Actor(
    char="@",
    color=color.white,
    name="Player",
    ai_cls=HostileEnemy,  # It is overriden, do not worry
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_defense=0, base_power=1),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=100)
)
# Enemies
mouse = Actor(
    char="m",
    color=color.light_gray,
    name="Mouse",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=0, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20)
)
rat = Actor(
    char="r",
    color=color.gray,
    name="Rat",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=0, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=40)
)
bat = Actor(
    char="b",
    color=color.dark_gray,
    name="Bat",
    ai_cls=BlindEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=1, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=50)
)
giant_rat = Actor(
    char="g",
    color=color.dark_gray,
    name="Giant Rat",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=5, base_defense=1, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100)
)
the_ratcatcher = Actor(
    char="K",
    color=color.red,
    name="The Ratcatcher",
    ai_cls=BossEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=2, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0)
)
# Items
# Consumables
pretzel = Item(
    char="!",
    color=color.brown,
    name="Pretzel",
    consumable=consumable.HealingConsumable(amount=4),
)
beer = Item(
    char="!",
    color=color.yellow,
    name="Beer",
    consumable=consumable.HealingConsumable(amount=20),
)  # hope this does not promote the wrong message, never forget to eat when drinking
rock = Item(
    char=".",
    color=color.gray,
    name="Rock",
    consumable=consumable.RangedDamageConsumable(damage=2, maximum_range=5),
)
carrot_flute = Item(
    char="~",
    color=color.orange,
    name="Carrot Flute",
    consumable=consumable.ConfusionConsumable(number_of_turns=5)
)
firebomb = Item(
    char=".",
    color=color.red,
    name="Firebomb",
    consumable=consumable.FirebombDamageConsumable(damage=6, radius=2)
)
# Equipment
# Equipment - weapons
wooden_stick = Item(
    char="/",
    color=color.brown,
    name="Wooden Stick",
    equippable=equippable.WoodenStick()
)
sword = Item(
    char="/",
    color=color.light_gray,
    name="Sword",
    equippable=equippable.Sword()
)
# Equipment - armor
leather_armor = Item(
    char="[",
    color=color.brown,
    name="Leather Armor",
    equippable=equippable.LeatherArmor()
)
chain_mail = Item(
    char="[",
    color=color.light_gray,
    name="Leather Armor",
    equippable=equippable.ChainMail()
)
