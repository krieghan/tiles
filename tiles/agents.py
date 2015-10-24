import zope.interface
import zope.interface.verify

from game_common import (
        interfaces,
        statemachine)
from game_common.twodee.geometry import (
        calculate,
        vector)

import tiles
from tiles import states

class MovingAgent(object):
    def __init__(self, 
                 world,
                 renderer,
                 height=1,
                 width=1,
                 tile=None):
        self.renderer = renderer
        self.height = height * tile.height
        self.width = width * tile.width
        self.tile = tile
        self.next_tile = None
        self.world = world
        self.tile = tile
        self.tile.add_member(self)
        if tile:
            self.position = tile.getPosition()
        else:
            return None

        self.state_machine = statemachine.StateMachine(
                owner=self,
                currentState=states.OnTile,
                globalState=None,
                name='tileMovement')

        self.state_machines = [self.state_machine]

        self.velocity = (0, 0)
        self.direction = None

    #Renderable
    def getActive(self):
        return True

    def getPosition(self):
        return self.position
    
    def getLength(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def draw(self):
        if self.renderer:
            self.renderer(self)

    #Moveable
    def getVelocity(self):
        return self.velocity
    
    def getSpeed(self):
        return vector.getMagnitude(self.velocity)

    def getHeading(self):
        return vector.normalize(self.velocity)

    def getDirectionDegrees(self):
        return vector.getDirectionDegrees(self.velocity)
    
    def getDirection(self):
        return vector.getDirectionRadians(self.velocity)

    def update(self, timeElapsed):
        for machine in self.get_state_machines():
            machine.update()

        self.position = calculate.addPointAndVector(
                self.position,
                self.velocity)

    #Observable
    def getObservers(self):
        return []

    def get_state_machines(self):
        return self.state_machines

    #TileInhabitant
    def change_tile(self, new_tile):
        self.tile.remove_member(self)
        self.tile = new_tile
        self.tile.add_member(self)
        self.next_tile = None

    def get_current_tile(self):
        return self.tile

    def is_obstructive(self):
        return False


class Enemy(MovingAgent):
    zope.interface.implements(
            [interfaces.Steerable,
             interfaces.Observable,
             tiles.TileInhabitant])

    def __init__(self,
                 world,
                 renderer,
                 height=1,
                 width=1,
                 tile=None):
        super(Enemy, self).__init__(
                world=world,
                renderer=renderer,
                height=height,
                width=width,
                tile=tile)

    def getMaxSpeed(self):
        return 10

    def getMaxForce(self):
        return 100

    def getObstacleDetectionDimensions(self):
        return None

    def getSteeringController(self):
        return None

class Player(MovingAgent):
    zope.interface.implements(
            [interfaces.Moveable,
             interfaces.Observable,
             tiles.TileInhabitant])

    def __init__(self, 
                 world,
                 renderer,
                 height=1,
                 width=1,
                 single_speed=5,
                 tile=None):
        super(Player, self).__init__(
                world=world,
                renderer=renderer,
                height=height,
                width=width,
                tile=tile)
        self.single_speed = single_speed

    #Moveable with binary speed (stopped or going)
    def setVelocityFromDirection(self, direction):
        self.velocity = vector.setMagnitude(direction, self.single_speed)

    def setSpeed(self, speed):
        self.velocity = vector.setMagnitude(self.velocity, speed)


zope.interface.verify.verifyClass(interfaces.Moveable, Player)
zope.interface.verify.verifyClass(interfaces.Observable, Player)
zope.interface.verify.verifyClass(tiles.TileInhabitant, Player)

zope.interface.verify.verifyClass(interfaces.Steerable, Enemy)
zope.interface.verify.verifyClass(interfaces.Observable, Enemy)
zope.interface.verify.verifyClass(tiles.TileInhabitant, Enemy)
