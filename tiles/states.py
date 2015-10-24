import zope.interface
import zope.interface.verify

from game_common import (
        constants,
        statemachine)

from game_common.twodee.geometry import vector

class AgentOnTile(object):
    zope.interface.implements(statemachine.IState)

    @classmethod
    def enter(cls, owner):
        owner.setSpeed(0)

    @classmethod
    def execute(cls, owner):
        owner.state_machine.changeState(AgentBetweenTiles)

    @classmethod
    def exit(cls, owner):
        pass

zope.interface.verify.verifyClass(statemachine.IState, AgentOnTile)

class AgentBetweenTiles(object):
    zope.interface.implements(statemachine.IState)

    @classmethod
    def enter(cls, owner):
        # Not bothering with calculating acceleration, here.
        # Velocity is the force vector at the magnitude of the 
        # owner's maximum speed
        force_vector = owner.steering_controller.calculate()
        
        # Pick the cardinal direction that's closest to the 
        # force vector
        cardinal_force = vector.pick_closest_vector(
                force_vector,
                [(0, 1), (0, -1), (-1, 0), (1, 0)])

        current_tile = owner.get_current_tile()
        next_tile = current_tile.getAdjacentTile(cardinal_force)
        if next_tile.is_obstructed():
            raise statemachine.StateChangeFailed()

        owner.set_next_tile(next_tile)
        owner.setVelocity(
                vector.setMagnitude(cardinal_force, owner.single_speed))

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
            owner.state_machine.changeState(AgentOnTile)

    @classmethod
    def exit(cls, owner):
        owner.change_tile(owner.next_tile)

zope.interface.verify.verifyClass(statemachine.IState, AgentBetweenTiles)

class OnTile(object):
    zope.interface.implements(statemachine.IState)

    @classmethod
    def enter(cls, owner):
        owner.setSpeed(0)

    @classmethod
    def execute(cls, owner):
        if owner.world.mode:
            owner.state_machine.changeState(BetweenTiles)

    @classmethod
    def exit(cls, owner):
        if owner.world.mode:
            current_tile = owner.get_current_tile()
            direction = constants.get_direction_from_gl_cursor(owner.world.mode)
            next_tile = current_tile.getAdjacentTile(direction)
            if next_tile.is_obstructed():
                raise statemachine.StateChangeFailed()

zope.interface.verify.verifyClass(statemachine.IState, OnTile)

class BetweenTiles(object):
    zope.interface.implements(statemachine.IState)

    @classmethod
    def enter(cls, owner):
        if owner.world.mode:
            currentTile = owner.tile
            owner.setVelocityFromDirection(
                constants.get_direction_from_gl_cursor(owner.world.mode))
            next_tile = currentTile.getAdjacentTile(owner.getHeading())
            owner.next_tile = next_tile

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
            owner.state_machine.changeState(OnTile)

    @classmethod
    def exit(cls, owner):
        owner.change_tile(owner.next_tile)

zope.interface.verify.verifyClass(statemachine.IState, BetweenTiles)

