from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import game.color as color
import game.exceptions as exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to"""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to deretermine its scope
        'self.engine' is the scope the action is being performed in
        'self.entity' is the object performing the action
        This method must be overriden by Action subclasses.
        """
        raise NotImplementedError()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class DelveAction(Action):
    def perform(self) -> None:
        """
        Take the stairs
        """
        # commented out if I'd like to make descending the staircase a button action instead of automatic
        # if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:

        # The code below is not a nice way of doing this. But it does do its job. Conversation system
        # and game text database coming soon in v0.2! (aka problem for future Dmitrij)
        self.engine.game_world.generate_floor()
        if self.engine.game_world.current_floor == 2:
            self.engine.message_log.add_message(
                'Not that the people of Hammeln were too kind to you. But you liked fishing.' +
                ' And they did buy your fish, which allowed you to catch more fish.' +
                ' It was a simple life, and you liked it. You want it back.',
                fg=color.welcome_text)
        elif self.engine.game_world.current_floor == 3:
            self.engine.message_log.add_message(
                '"As you delve into the middle level of the dungeon, you notice a sombre tune ' +
                'sometimes emerging above the ever-present rat squeaks.',
                fg=color.welcome_text)
        elif self.engine.game_world.current_floor == 4:
            self.engine.message_log.add_message(
                '"The music intensifies. In most people, it would bring out an intense longing for...' +
                ' well, what does it matter? You are not most people. You just care about catching fish.' +
                ' Getting close, based fisherman.',
                fg=color.welcome_text)
        elif self.engine.game_world.current_floor == 5:
            self.engine.message_log.add_message(
                'A tall, wiry character in gray stands before you. You look into his dark eyes.' +
                '"This place, these times... everyone gets corrupted sooner or later, no matter how honest," he says, picks up his flute and' +
                " starts to play a sad magic melody - which has no effect on you.",
                fg=color.welcome_text)
        # else:
        #    raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns the actions' destination"""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Returns the blocking entity ad the actions' destination"""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions' destination"""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @property
    def target_item(self) -> Optional[Item]:
        """Return the item at this actions' destination"""
        return self.engine.game_map.get_item_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class BossSpecialAttack(Action):

    def perform(self, target) -> None:
        self.target = target

        damage = 5  # flutes do true damage haha

        attack_desc = f"{self.entity.name} throws his flute at you for 5 hit points!"
        attack_color = color.enemy_atk
        self.engine.message_log.add_message(attack_desc, attack_color)
        self.target.fighter.hp -= damage

    # either create a new component of abilities, or on expanding the game
    # there will be too many actions when defining special enemy attacks!


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination not walkable
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination blocked by entity
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        elif self.target_item:
            return PickupAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class BlindEnemyAction(ActionWithDirection):
    """ The actor will either try to move or attack in the chosen direction
        In case the actor bumps into a wall, a turn is just wasted
        A blind enemy won't atack other enemies, just the player"""

    def perform(self) -> None:
        if self.target_actor == self.engine.player:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        elif self.target_actor and ~(self.target_actor == self.engine.player):
            return WaitAction(self.entity).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class PickupAction(ActionWithDirection):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def perform(self) -> None:
        item = self.target_item
        inventory = self.engine.player.inventory

        if len(inventory.items) >= inventory.capacity:
            raise exceptions.Impossible("Your inventory is full.")

        self.engine.game_map.entities.remove(item)
        item.parent = self.entity.inventory
        inventory.items.append(item)

        self.engine.message_log.add_message(f"You picked up the {item.name}.")
        return MovementAction(self.entity, self.dx, self.dy).perform()
        #raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):

    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)
