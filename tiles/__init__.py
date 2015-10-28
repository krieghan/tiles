from OpenGL import GL
import zope.interface
import zope.interface.verify

from game_common import (
        interfaces,
        graph)

from tiles import constants

def get_tile_factory(height_in, width_in):
    class Tile(object):
        zope.interface.implements([
            interfaces.Renderable,
            graph.NodeData])

        height = height_in
        width = width_in

        def __init__(self, grid, w_index, h_index):
            self.grid = grid
            self.x = w_index
            self.y = h_index
            self.position = ((w_index + .5) * self.width,
                             (h_index + .5) * self.height)

            self.members = set()
            self.node = None
            
        def set_graph_node(self, node):
            self.node = node

        def get_graph_node(self):
            return self.node

        def add_member(self, member):
            self.members.add(member)

        def remove_member(self, member):
            self.members.remove(member)

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

        def is_obstructed(self):
            for member in self.members:
                if member.is_obstructive():
                    return True
                
            return False

        def is_traversable(self):
            return not self.is_obstructed()

    zope.interface.verify.verifyClass(interfaces.Renderable, Tile)
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


