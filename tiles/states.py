import zope.interface
import zope.interface.verify

from game_common import statemachine 

class OnTile(object):
    zope.interface.implements(statemachine.IState)

    def enter(self, owner):
        pass

    def execute(self, owner):
        if owner.world.mode:
            owner.state_machine.changeState(BetweenTiles)

    def exit(self, owner):
        pass

zope.interface.verify.verifyClass(statemachine.IState, OnTile)

def BetweenTiles(object):
    zope.interface.implements(statemachine.IState)

    def enter(self, owner):
        if owner.world.mode:
            steeringController = owner.steeringController
            currentTile = owner.tile
            nextTile = currentTile.getAdjacentTile(owner.world.mode)
            steeringController.activate(
                    'seek',
                    nextTile.getPosition())


    def execute(self, owner):
        (owner_x, owner_y) = owner.getPosition()
        (tile_x, tile_y) = owner.next_tile.getPosition()
        arrived = False
        if owner.direction == constants.UP:
            arrived = owner_y >= tile_y
        elif owner.direction == constants.DOWN:
            arrived = owner_y <= tile_y
        elif owner.direction == constants.LEFT:
            arrived = owner_x <= tile_x
        elif owner.direction == constants.RIGHT:
            arrived = owner_x >= tile_x

        if arrived:
            owner.state_machine.changeState(OnTile)

    def exit(self, owner):
        owner.steeringController.deactivate('seek')

zope.interface.verify.verifyClass(statemachine.IState, BetweenTiles)

