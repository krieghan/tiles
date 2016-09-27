import zope.interface
import zope.interface.verify

from game_common import interfaces
from game_common.twodee.geometry import intersect
import tiles

class Obstacle(object):
    zope.interface.implements(
            [tiles.TileInhabitant,
             interfaces.Collideable,
             interfaces.Renderable])

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
        self.tile.add_member(self)

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

    # TileInhabitant
    def get_current_tile(self):
        return self.tile

    def is_obstructive(self):
        return True

    # Collideable
    def getBoundaries(self):
        half_height = self.height / 2.0
        half_width = self.width / 2.0
        return {intersect.Rectangle : (
                    (-half_width, -half_height),
                    (half_width, -half_height),
                    (half_width, half_height),
                    (-half_width, half_height))}

    def handleCollision(self, otherElement):
        pass

    def getDirection(self):
        return 0

zope.interface.verify.verifyClass(interfaces.Renderable, Obstacle)
zope.interface.verify.verifyClass(interfaces.Collideable, Obstacle)
zope.interface.verify.verifyClass(tiles.TileInhabitant, Obstacle)

