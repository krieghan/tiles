from game_common import (
        constants,
        statemachine)
from game_common.twodee.geometry import (
        vector,
        calculate)
from zope.interface import implementer, verify


@implementer(statemachine.IState)
class AgentOnTile(object):
    @classmethod
    def enter(cls, owner):
        owner.setSpeed(0)

    @classmethod
    def execute(cls, owner):
        owner.state_machine.change_state(AgentBetweenTiles)

    @classmethod
    def exit(cls, owner):
        pass

verify.verifyClass(statemachine.IState, AgentOnTile)


@implementer(statemachine.IState)
class AgentBetweenTiles(object):
    @classmethod
    def enter(cls, owner):
        owner.update_path()
        path = owner.get_path()
        next_tile = owner.get_current_tile()

        while next_tile is owner.get_current_tile():
            if len(path) == 0:
                raise statemachine.StateChangeFailed()
            next_tile = path.pop(0)

        if next_tile.is_obstructed():
            raise statemachine.StateChangeFailed()

        owner_to_tile = calculate.subtractPoints(
                next_tile.getPosition(),
                owner.getPosition())

        # Pick the cardinal direction that's closest to the 
        # force vector
        cardinal_velocity = vector.pick_closest_vector(
                owner_to_tile,
                [(0, 1), (0, -1), (-1, 0), (1, 0)])

        owner.set_next_tile(next_tile)
        owner.setVelocity(
                vector.setMagnitude(
                    cardinal_velocity, 
                    owner.single_speed))

    @classmethod
    def execute(cls, owner):
        (owner_x, owner_y) = owner.getPosition()
        next_tile = owner.get_next_tile()
        (tile_x, tile_y) = next_tile.getPosition()
        arrived = False
        direction = owner.getHeading()
        if direction == (0, 1):
            arrived = owner_y >= tile_y
        elif direction == (0, -1):
            arrived = owner_y <= tile_y
        elif direction == (-1, 0):
            arrived = owner_x <= tile_x
        elif direction == (1, 0):
            arrived = owner_x >= tile_x

        if arrived:
            owner.position = (tile_x, tile_y)
            owner.state_machine.change_state(AgentOnTile)

    @classmethod
    def exit(cls, owner):
        owner.change_tile(owner.next_tile)

verify.verifyClass(statemachine.IState, AgentBetweenTiles)


@implementer(statemachine.IState)
class OnTile(object):
    @classmethod
    def enter(cls, owner):
        owner.setSpeed(0)

    @classmethod
    def execute(cls, owner):
        if owner.world.mode:
            owner.state_machine.change_state(BetweenTiles)

    @classmethod
    def exit(cls, owner):
        if owner.world.mode:
            current_tile = owner.get_current_tile()
            direction = constants.get_direction_from_gl_cursor(owner.world.mode)
            next_tile = current_tile.getAdjacentTile(direction)
            if next_tile is None:
                raise statemachine.StateChangeFailed()
            if next_tile.is_obstructed():
                raise statemachine.StateChangeFailed()

verify.verifyClass(statemachine.IState, OnTile)

@implementer(statemachine.IState)
class BetweenTiles(object):
    @classmethod
    def enter(cls, owner):
        if owner.world.mode:
            currentTile = owner.tile
            owner.setVelocityFromDirection(
                constants.get_direction_from_gl_cursor(owner.world.mode))
            next_tile = currentTile.getAdjacentTile(owner.getHeading())
            owner.set_next_tile(next_tile)

    @classmethod
    def execute(cls, owner):
        (owner_x, owner_y) = owner.getPosition()
        (tile_x, tile_y) = owner.next_tile.getPosition()
        arrived = False
        direction = owner.getHeading()
        if direction == (0, 1):
            arrived = owner_y >= tile_y
        elif direction == (0, -1):
            arrived = owner_y <= tile_y
        elif direction == (-1, 0):
            arrived = owner_x <= tile_x
        elif direction == (1, 0):
            arrived = owner_x >= tile_x

        if arrived:
            owner.position = (tile_x, tile_y)
            owner.state_machine.change_state(OnTile)

    @classmethod
    def exit(cls, owner):
        owner.change_tile(owner.next_tile)

verify.verifyClass(statemachine.IState, BetweenTiles)

