import zope.interface
import zope.interface.verify

from game_common import interfaces

class Obstacle(object):
    zope.interface.implements(interfaces.Renderable)

    def __init__(self,
                 world,
                 renderer,
                 height,
                 width,
                 tile):
        self.world = world
        self.renderer = renderer
        self.height = height * tile.height
        self.width = width * tile.width
        self.tile = tile
        self.position = tile.getPosition()

    def getPosition(self):
        return self.position

    def getLength(self):
        return self.height

    def getWidth(self):
        return self.width

    def update(self, timeElapsed):
        pass

    def draw(self):
        self.renderer(self)

    def getActive(self):
        return True

zope.interface.verify.verifyClass(interfaces.Renderable, Obstacle)

