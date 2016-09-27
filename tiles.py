import optparse

from tiles import tiles_world
from game_common import canvas

def run():
    world = tiles_world.TilesWorld(
                height_tiles=10,
                width_tiles=10,
                tile_height=100,
                tile_width=100)
    tiles_canvas = canvas.Canvas(
            world=world,
            title='Tiles')
    tiles_canvas.start()

if __name__ == "__main__":
    run()
