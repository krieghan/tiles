import zope.interface
import zope.interface.verify

from game_common import (
        constants,
        statemachine)

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
        pass

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
        owner.tile = owner.next_tile
        owner.next_tile = None

zope.interface.verify.verifyClass(statemachine.IState, BetweenTiles)

