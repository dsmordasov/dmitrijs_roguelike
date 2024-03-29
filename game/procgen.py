from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import tcod

import game.entity_factories as entity_factories
from game.game_map import GameMap
import game.tile_types as tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

max_items_by_floor = [
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 1),
    (5, 0) # Makes sure no items are spawned on boss floor
]

max_monsters_by_floor = [
    (1, 7),
    (2, 6),
    (3, 6),
    (4, 3),
    (5, 1)
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    1: [(entity_factories.pretzel, 60), (entity_factories.rock, 40)],
    2: [(entity_factories.pretzel, 20), (entity_factories.rock, 10),
        (entity_factories.wooden_stick, 35), (entity_factories.leather_armor, 35)],
    3: [(entity_factories.pretzel, 50), (entity_factories.rock, 5),
        (entity_factories.wooden_stick, 10), (entity_factories.leather_armor, 10),
        (entity_factories.carrot_flute, 5), (entity_factories.firebomb, 20)],
    4: [(entity_factories.beer, 10), (entity_factories.firebomb, 10), 
        (entity_factories.sword, 40), (entity_factories.chain_mail, 40)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    1: [(entity_factories.mouse, 100)],
    2: [(entity_factories.mouse, 20), (entity_factories.rat, 80)],
    3: [(entity_factories.mouse, 0), (entity_factories.rat, 70),\
         (entity_factories.bat, 20), (entity_factories.giant_rat, 10)],
    4: [(entity_factories.mouse, 0), (entity_factories.rat, 20),\
         (entity_factories.bat, 20), (entity_factories.giant_rat, 60)],
}

def get_max_value_for_floor(
    weighted_chances_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in weighted_chances_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value
    
    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance
    
    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property # Returns and sets read-only variables for the class
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Returns True if this room overlaps with another RectangularRoom"""
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def place_entities(
    room: RectangularRoom, 
    dungeon: GameMap, 
    floor_number: int,
) -> None:
    number_of_monsters = random.randint(0, get_max_value_for_floor(max_monsters_by_floor, floor_number))
    number_of_items = random.randint(0, get_max_value_for_floor(max_items_by_floor, floor_number))

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )
    
    for entity in (monsters + items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if (not any(entity.x == x and entity.y == y for entity in dungeon.entities))\
             and (dungeon.tiles[(x, y)] != tile_types.down_stairs):
            entity.spawn(dungeon, x, y)

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: # A 50% chance
        corner_x, corner_y = x2, y1 # Move horizontally, then vertically
    else:
        corner_x, corner_y = x1, y2 # Move vertically, then horizontally
    
    # Generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map"""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles a pleasure to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms to check for intersections
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # There is intersection, so try another room
        # If there is no intersection, the room is valid, so continue

        # Dig out this rooms' inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0: # First room, player spawn
            player.place(*new_room.center, dungeon) 
        else: # All rooms after the first one
            # Dig out a tunnel between this room and the previous one
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
            
            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)
        
        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        rooms.append(new_room)
    
    return dungeon

def generate_end_level(
    map_width: int, 
    map_height: int,
    engine: Engine,
    ) -> GameMap:
    # Generate end level
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    x = round(dungeon.width/2 - dungeon.width/4)
    y = round(dungeon.height/2)

    boss_room_width = 15
    boss_room_height = 10

    boss_room = RectangularRoom(x, y, boss_room_width, boss_room_height)
    dungeon.tiles[boss_room.inner] = tile_types.floor

    player_spawnpoint = ((x+2), round(y+boss_room_height/2))
    boss_spawnpoint = ((x+10), round(y+boss_room_height/2))

    # The order of arguments in the two lines below physically hurt
    player.place(*player_spawnpoint, dungeon)
    entity_factories.the_ratcatcher.spawn(dungeon, *boss_spawnpoint)

    # actually this whole boss room hurts me, so much hardcode and the boss room -
    # just a rectangle, really? but damn do I want something finishable
    # please forgive me if you do any bit of game dev and are looking through this
    return dungeon
    

