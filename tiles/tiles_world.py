import sys
import time

from game_common import (
        graph,
        interfaces)
from game_common.twodee.geometry import intersect
from OpenGL import GL, GLUT
from zope.interface import (
    implementer,
    verify)

import tiles
from tiles import (
        agents, 
        renderers, 
        props)

@implementer(interfaces.IWorld)
class TilesWorld(object):
    def __init__(self,
                 height_tiles,
                 width_tiles,
                 tile_height,
                 tile_width):
        self.canvasElements = set()
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

        TileFactory = tiles.get_tile_factory(
                        height_in=self.tile_height,
                        width_in=self.tile_width)

        self.tiles = []
        for w in range(width_tiles):
            self.tiles.append([])
            for h in range(height_tiles):
                tile = TileFactory(self.tiles, w, h)
                tile_node = graph.Node(data=tile)
                tile.set_graph_node(tile_node)
                adjacent_tiles = tile.getAllAdjacentTiles()
                for adjacent_tile in adjacent_tiles:
                    tile_node.add_two_way_connected_node(adjacent_tile.get_graph_node())

                self.canvasElements.add(tile)
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

        enemy = agents.Enemy(
                world=self,
                renderer=renderers.render_enemy,
                height=.8,
                width=.8,
                tile=self.tiles[0][0])

        enemy.set_target(self.player)

        enemy.getSteeringController().activate('pursue', self.player)
                
        self.add_canvas_element(self.player)
        self.add_canvas_element(obstacle)
        self.add_canvas_element(enemy)
        self.mode = None

    def getHeightWidth(self):
        return (self.height, self.width)

    def getMaxLeftRightBottomTop(self):
        return (self.max_left,
                self.max_right,
                self.max_bottom,
                self.max_top)

    def add_canvas_element(self, element):
        verify.verifyObject(
                interfaces.Collideable,
                element)
        verify.verifyObject(
                interfaces.Renderable,
                element)
        self.canvasElements.add(element)

    def remove_canvas_element(self, element):
        self.canvasElements.remove(element)

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
        for canvasElement in list(self.getAllCanvasElements()):
            if not canvasElement.getActive():
                continue
            canvasElement.update(timeElapsed=timeElapsed)

        cleared_of_collisions = set([])

        for canvasElement in list(self.getAllCanvasElements()):
            for otherElement in list(self.getAllCanvasElements()):
                if canvasElement is otherElement:
                    continue
                
                # Don't double-count collisions when canvasElement
                # is reconsidered as otherElement
                if otherElement in cleared_of_collisions:
                    continue

                if intersect.collidesWith(canvasElement, otherElement):
                    canvasElement.handleCollision(otherElement)
                    otherElement.handleCollision(canvasElement)

            cleared_of_collisions.add(canvasElement)

    def render(self):
        for element in self.getAllCanvasElements():
            element.draw()
    
    def getAllCanvasElements(self):
        return self.canvasElements

verify.verifyClass(interfaces.IWorld, TilesWorld)
