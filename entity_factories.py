from components.ai import BlindEnemy, ConfusedEnemy, HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item
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
    char="r", 
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
    char="g", 
    color=(63, 127, 63), 
    name="The Rat Catcher",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=2, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0)
    )
# Items
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)
confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=5)
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3)
)
# Equipment
# Equipment - weapons
dagger = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger()
)
sword = Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword()
)
# Equipment - armor
leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor()
)
chain_mail = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.ChainMail()
)