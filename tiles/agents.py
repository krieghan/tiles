import zope.interface
import zope.interface.verify

from game_common import (
        interfaces,
        statemachine)
from game_common.twodee.geometry import (
        calculate,
        vector)

from tiles import states

class Player(object):
    zope.interface.implements(
            [interfaces.Moveable,
             interfaces.Observable])

    def __init__(self, 
                 world=None,
                 renderer=None,
                 height=10,
                 width=10,
                 single_speed=5,
                 tile=None):
        self.renderer = renderer
        self.height = height
        self.width = width
        self.active = True
        self.tile = tile
        self.next_tile = None
        self.single_speed = single_speed
        self.world = world
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
    def getPosition(self):
        return self.position
    
    def getLength(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def update(self, timeElapsed):
        for machine in self.state_machines:
            machine.update()

        self.position = calculate.addPointAndVector(
                self.position,
                self.velocity)

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

    #Observable
    def getObservers(self):
        return []

    #Moveable with binary speed (stopped or going)
    def setVelocityFromDirection(self, direction):
        self.velocity = vector.setMagnitude(direction, self.single_speed)


zope.interface.verify.verifyClass(interfaces.Moveable, Player)
zope.interface.verify.verifyClass(interfaces.Observable, Player)
