import optparse

from tiles import canvas

def run():
    world = canvas.TilesWorld(height=100000,
                               width=100000)
    escape_canvas = canvas.TilesCanvas(world=world)
    escape_canvas.start()


if __name__ == "__main__":
    run()
