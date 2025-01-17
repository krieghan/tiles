from OpenGL import GL
from game_common import (
        interfaces,
        graph)
import zope.interface
from zope.interface import (
    implementer,
    verify)

from tiles import constants

def get_tile_factory(height_in, width_in):
    @implementer(
        interfaces.Renderable,
        interfaces.Collideable,
        graph.NodeData)
    class Tile(object):
        height = height_in
        width = width_in

        def __init__(self, grid, w_index, h_index):
            self.grid = grid
            self.x = w_index
            self.y = h_index
            self.position = ((w_index + .5) * self.width,
                             (h_index + .5) * self.height)

            self.members = set()
            self.aspiring_members = set()
            self.node = None
            
        def set_graph_node(self, node):
            self.node = node

        def get_graph_node(self):
            return self.node

        def get_grid_position(self):
            return (self.x, self.y)

        def add_member(self, member):
            self.members.add(member)

        def remove_member(self, member):
            self.members.remove(member)

        def add_aspiring_member(self, member):
            self.aspiring_members.add(member)

        def remove_aspiring_member(self, member):
            self.aspiring_members.remove(member)

        def getActive(self):
            return True

        def getWidth(self):
            return self.width

        def getLength(self):
            return self.height

        def getPosition(self):
            return self.position

        def update(self, timeElapsed):
            pass

        def draw(self):
            x, y = self.getPosition()
            half_width = .5 * self.width
            half_height = .5 * self.height
            color = (1, 1, 1)

            GL.glPushMatrix()
            GL.glTranslate(x, y, 0)
            GL.glColor3f(*color)
            GL.glBegin(GL.GL_LINE_LOOP)

            GL.glVertex2f(-half_width, half_height)
            GL.glVertex2f(half_width, half_height)
            GL.glVertex2f(half_width, -half_height)
            GL.glVertex2f(-half_width, -half_height)

            GL.glEnd()
            GL.glPopMatrix()

        def getAdjacentTile(self, direction):
            new_x = self.x
            new_y = self.y
            new_x = int(new_x + direction[0])
            new_y = int(new_y + direction[1])

            if new_x < 0 or new_y < 0:
                return None

            try:
                return self.grid[new_x][new_y]
            except IndexError:
                return None

        def getAllAdjacentTiles(self):
            tiles = []
            for direction in constants.directions:
                tile = self.getAdjacentTile(direction)
                if tile is not None:
                    tiles.append(tile)
            return tiles

        def getBoundaries(self):
            return {}

        def handleCollision(self, other):
            pass

        def getDirection(self):
            return 0

        def is_obstructed(self):
            for member in self.members.union(self.aspiring_members):
                if member.is_obstructive():
                    return True
                
            return False

        def is_traversable(self):
            return not self.is_obstructed()

        def calculate_heuristic_cost(self, target_tile):
            my_x, my_y = self.get_grid_position()
            target_x, target_y = target_tile.get_grid_position()
            return abs(my_x - target_x) + abs(my_y - target_y)


    verify.verifyClass(interfaces.Renderable, Tile)
    verify.verifyClass(interfaces.Collideable, Tile)
    verify.verifyClass(graph.NodeData, Tile)
    return Tile

class TileInhabitant(zope.interface.Interface):
    def get_current_tile():
        pass

    def is_obstructive():
        pass

class TileAgent(TileInhabitant):
    def change_tile(new_tile):
        pass

    def set_next_tile():
        pass

    def get_next_tile():
        pass


