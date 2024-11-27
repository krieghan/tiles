from game_common import (
        interfaces,
        statemachine,
        graph)
from game_common.twodee.geometry import (
        calculate,
        intersect,
        vector)
from game_common.twodee.steering import steeringcontroller
from zope.interface import (implementer, verify)

import tiles
from tiles import states, renderers

class MovingAgent(object):
    def __init__(self, 
                 world,
                 renderer,
                 height=1,
                 width=1,
                 position=None,
                 tile=None):
        self.renderer = renderer
        self.height = height * tile.height
        self.width = width * tile.width
        self.tile = tile
        self.next_tile = None
        self.world = world
        self.tile = tile
        self.tile.add_member(self)
        if position is None:
            if tile:
                self.position = tile.getPosition()
            else:
                raise Exception('No position for agent')
        else:
            self.position = position
                
        self.state_machines = []

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

    def getBoundaries(self):
        return {intersect.Circle: ((0, 0), self.getLength() / 2.0)}

    def draw(self):
        if self.renderer:
            self.renderer(self)

    #Moveable
    def setVelocity(self, velocity):
        self.velocity = velocity

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
        self.set_next_tile(None)

    def get_current_tile(self):
        return self.tile

    def set_next_tile(self, next_tile):
        if self.next_tile:
            self.next_tile.remove_aspiring_member(self)

        self.next_tile = next_tile
        if next_tile is not None:
            next_tile.add_aspiring_member(self)

    def get_next_tile(self):
        return self.next_tile

    def is_obstructive(self):
        return True

    #Moveable with binary speed (stopped or going)
    def setVelocityFromDirection(self, direction):
        self.velocity = vector.setMagnitude(direction, self.single_speed)

    def setSpeed(self, speed):
        self.velocity = vector.setMagnitude(self.velocity, speed)

@implementer(
    interfaces.Moveable,
    interfaces.Observable,
    interfaces.Collideable,
    tiles.TileAgent)
class Shot(MovingAgent):
    def __init__(self,
                 world,
                 direction,
                 owner,
                 renderer=renderers.render_shot,
                 height=.2,
                 width=.2,
                 single_speed=10,
                 position=None,
                 tile=None):
        super(Shot, self).__init__(
                world=world,
                renderer=renderer,
                height=height,
                width=width,
                position=position,
                tile=tile)
        self.owner = owner
        self.single_speed = single_speed
        self.velocity = vector.setMagnitude(
                direction,
                self.single_speed)
        
    def is_obstructive(self):
        return False

    def update(self, timeElapsed):
        super(Shot, self).update(timeElapsed)

    def handleCollision(self, otherElement):
        if otherElement is self.owner:
            return
        self.world.remove_canvas_element(self)


@implementer(
    interfaces.Steerable,
    interfaces.Observable,
    interfaces.Collideable,
    tiles.TileAgent)
class Enemy(MovingAgent):
    def __init__(self,
                 world,
                 renderer,
                 height=1,
                 width=1,
                 single_speed=4,
                 tile=None):
        super(Enemy, self).__init__(
                world=world,
                renderer=renderer,
                height=height,
                width=width,
                tile=tile)
        self.steering_controller = steeringcontroller.SteeringController(
                agent=self)
        self.single_speed = single_speed

        self.state_machine = statemachine.StateMachine(
                owner=self,
                current_state=states.AgentOnTile,
                global_state=None,
                name='tileMovement')
        self.state_machines.append(self.state_machine)
        self.target = None
        self.path = []
        self.shotCooldown = 1000
        self.timeSinceLastShot = self.shotCooldown
        
    
    def handleCollision(self, otherElement):
        pass

    def getMaxSpeed(self):
        return self.single_speed

    def getMaxForce(self):
        return 100

    def getObstacleDetectionDimensions(self):
        return None

    def getSteeringController(self):
        return self.steering_controller

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target
        self.update_path()

    def get_path(self):
        return self.path

    def update_path(self):
        if not self.target:
            return

        if (self.path is None or 
            self.path == [] or
            self.path[-1] is not self.target.get_current_tile()):
            current_node = self.get_current_tile().get_graph_node()
            target_node = self.target.get_current_tile().get_graph_node()
            path_of_nodes = graph.get_path_to_target(
                    current_node,
                    target_node)
            self.path = [node.get_data() for node in path_of_nodes]

    def update(self, timeElapsed):
        self.timeSinceLastShot += timeElapsed
        if self.timeSinceLastShot >= self.shotCooldown:
            self.timeSinceLastShot = 0
            tile = self.get_current_tile()
            target_tile = self.target.get_current_tile()
            x, y = tile.get_grid_position()
            target_x, target_y = target_tile.get_grid_position()
            if target_x == x or target_y == y:
                if target_x == x:
                    if y < target_y:
                        direction = (0, 1)
                    else:
                        direction = (0, -1)
                    agent_to_origination_point = vector.setMagnitude(
                            direction,
                            self.height * .5)
                if target_y == y:
                    if x < target_x:
                        direction = (1, 0)
                    else:
                        direction = (-1, 0)
                    agent_to_origination_point = vector.setMagnitude(
                            direction,
                            self.width * .5)

                origination_point = calculate.addPointAndVector(
                        self.position,
                        agent_to_origination_point)

                shot = Shot(world=self.world,
                            direction=direction,
                            tile=tile,
                            owner=self,
                            position=origination_point)
                self.world.add_canvas_element(shot)

        super(Enemy, self).update(self)

@implementer(
    interfaces.Moveable,
    interfaces.Observable,
    interfaces.Collideable,
    tiles.TileAgent)
class Player(MovingAgent):
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

        self.state_machine = statemachine.StateMachine(
                owner=self,
                current_state=states.OnTile,
                global_state=None,
                name='tileMovement')
        self.state_machines.append(self.state_machine)

    def handleCollision(self, otherElement):
        pass

verify.verifyClass(interfaces.Moveable, Player)
verify.verifyClass(interfaces.Observable, Player)
verify.verifyClass(interfaces.Collideable, Player)
verify.verifyClass(tiles.TileInhabitant, Player)

verify.verifyClass(interfaces.Steerable, Enemy)
verify.verifyClass(interfaces.Observable, Enemy)
verify.verifyClass(interfaces.Collideable, Enemy)
verify.verifyClass(tiles.TileInhabitant, Enemy)

verify.verifyClass(interfaces.Moveable, Shot)
verify.verifyClass(interfaces.Observable, Shot)
verify.verifyClass(interfaces.Collideable, Shot)
verify.verifyClass(tiles.TileInhabitant, Shot)
