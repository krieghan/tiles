import zope.interface
import zope.interface.verify

from game_common import (
        interfaces,
        statemachine)

from tiles import states

class Player(object):
    zope.interface.implements(interfaces.Steerable)

    def __init__(self, 
                 world=None,
                 renderer=None,
                 height=10,
                 width=10,
                 tile=None):
        self.renderer = renderer
        self.height = height
        self.width = width
        self.active = True
        self.tile = tile
        self.next_tile = None
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

        self.steeringController = steeringcontroller.SteeringController(
                owner=self)

        self.velocity = (0, 0)
        self.direction = None

    def draw(self):
        if self.renderer:
            self.renderer(self)

    def getPosition(self):
        return self.position
    
    def getLength(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def update(self, timeElapsed):
        pass

    def getVelocity(self):
        return self.velocity
    
    def getSpeed(self):
        return 0
    
    def getHeading(self):
        pass

    def getDirectionDegrees(self):
        pass
    
    def getDirection(self):
        pass

    def getMaxSpeed(self):
        pass
    
    def getMaxForce(self):
        pass
    
    def getObstacleDetectionDimensions(self):
        pass
    
    def getSteeringController(self):
        pass

zope.interface.verify.verifyClass(interfaces.Steerable, Agent)
