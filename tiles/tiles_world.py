import sys
import time

from OpenGL import GL
import zope.interface 
import zope.interface.verify

from game_common import interfaces

class TilesWorld(object):

    zope.interface.implements(interfaces.IWorld)

    def __init__(self,
                 height_tiles,
                 width_tiles,
                 tile_height,
                 tile_width):
        self.canvasElements = []
        self.height_tiles = height_tiles
        self.width_tiles = width_tiles
        self.tile_height = tile_height
        self.tile_width = tile_width

        self.height = height_tiles * tile_height
        self.width = width_tiles * tile_width

        self.max_left = 0
        self.max_right = self.width
        self.max_bottom = 0
        self.max_top = self.height

        self.current_time = 0

        TileFactory = get_tile_factory(height_in=self.tile_height,
                                       width_in=self.tile_width)

        self.tiles = []
        for h in range(height_tiles):
            self.tiles.append([])
            for w in range(width_tiles):
                tile = TileFactory(h, w)
                self.canvasElements.append(tile)
                self.tiles[h].append(tile)

    def update(self,
               currentTime):
        if not self.current_time:
            self.current_time = currentTime
        timeElapsed = (currentTime - self.current_time)
        self.current_time = currentTime
        for canvasElement in self.getAllCanvasElements():
            if not canvasElement.active:
                continue
            canvasElement.update(timeElapsed=timeElapsed)

    def render(self):
        for element in self.getAllCanvasElements():
            element.draw()
    
    def getAllCanvasElements(self):
        return self.canvasElements

zope.interface.verify.verifyClass(interfaces.IWorld, TilesWorld)

def get_tile_factory(height_in, width_in):
    class Tile(object):
        zope.interface.implements(interfaces.Renderable)

        height = height_in
        width = width_in

        def __init__(self, h_index, w_index):
            self.active = True
            self.position = ((w_index + .5) * self.width,
                             (h_index + .5) * self.height)
            
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

    zope.interface.verify.verifyClass(interfaces.Renderable, Tile)
    return Tile


