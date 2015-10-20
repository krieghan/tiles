import sys
import time

from OpenGL import GL, GLUT
import zope.interface 
import zope.interface.verify

from game_common import interfaces
from tiles import agents, renderers, props

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
        for w in range(width_tiles):
            self.tiles.append([])
            for h in range(height_tiles):
                tile = TileFactory(self.tiles, w, h)
                self.canvasElements.append(tile)
                self.tiles[w].append(tile)

        self.player = agents.Player(
                world=self,
                renderer=renderers.render_player,
                height=.8,
                width=.8,
                tile=self.tiles[4][5])

        obstacle = props.Obstacle(
                world=self,
                renderer=renderers.render_obstacle,
                height=1,
                width=1,
                tile=self.tiles[3][3])
                
        self.canvasElements.append(self.player)
        self.canvasElements.append(obstacle)
        self.mode = None

    def start(self):
        GLUT.glutIgnoreKeyRepeat(True)
        GLUT.glutSpecialFunc(self.special_keyboard_down)
        GLUT.glutSpecialUpFunc(self.special_keyboard_up)

    def special_keyboard_down(self, key, mouse_x, mouse_y):
        if key in (GLUT.GLUT_KEY_UP, 
                   GLUT.GLUT_KEY_DOWN,
                   GLUT.GLUT_KEY_LEFT,
                   GLUT.GLUT_KEY_RIGHT):
            self.mode = key

    def special_keyboard_up(self, key, mouse_x, mouse_y):
        if key in (GLUT.GLUT_KEY_UP, 
                   GLUT.GLUT_KEY_DOWN,
                   GLUT.GLUT_KEY_LEFT,
                   GLUT.GLUT_KEY_RIGHT):
            if key == self.mode:
                self.mode = None

    def update(self,
               currentTime):
        if not self.current_time:
            self.current_time = currentTime
        timeElapsed = (currentTime - self.current_time)
        self.current_time = currentTime
        for canvasElement in self.getAllCanvasElements():
            if not canvasElement.getActive():
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

        def __init__(self, grid, w_index, h_index):
            self.grid = grid
            self.x = w_index
            self.y = h_index
            self.position = ((w_index + .5) * self.width,
                             (h_index + .5) * self.height)
            
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

            return self.grid[new_x][new_y]

        

    zope.interface.verify.verifyClass(interfaces.Renderable, Tile)
    return Tile

