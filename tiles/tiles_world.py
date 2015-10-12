import sys
import time

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

        TileFactory = get_tile_factory(length_in=self.tile_height,
                                       width_in=self.tile_width)

        self.tiles = []
        for h in range(height_tiles):
            self.tiles.append([])
            for w in range(width_tiles):
                tile = TileFactory()
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


def get_tile_factory(length_in, width_in):
    class Tile(object):
        zope.interface.implements(interfaces.Renderable)

        length = length_in
        width = width_in

        def __init__(self):
            self.active = True

        def getWidth(self):
            return self.width

        def getLength(self):
            return self.length

        def getPosition(self):
            return None

        def update(self, timeElapsed):
            pass

        def draw(self):
            pass

    zope.interface.verify.verifyClass(interfaces.Renderable, Tile)
    return Tile


