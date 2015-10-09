import sys
import time

from OpenGL import GL, GLU, GLUT

class TilesWorld(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.max_left = 0
        self.max_right = width
        self.max_bottom = 0
        self.max_top = height

        self.current_time = 0

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
        return ()

class TilesCanvas(object):
    def __init__(self,
                 world):
        self.world = world
        self.time_interval = 10
        GLUT.glutInit(sys.argv)
        self.lastTime = GLUT.glutGet(GLUT.GLUT_ELAPSED_TIME)
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | 
                                 GLUT.GLUT_RGB | 
                                 GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(500,500)
        GLUT.glutCreateWindow('Tiles')
        GLUT.glutDisplayFunc(self.render)
        GLUT.glutReshapeFunc(self.onSize)

        self.init = False
        
        #initialized to actual values in setupView
        self.viewport_left = 0
        self.viewport_bottom = 0
        self.viewport_height = 0
        self.viewport_width = 0
        
        self.timeStep = 1
        self.timeElapsed = self.time_interval / 1000.0

    def start(self):
        self.InitGL()
        GLUT.glutTimerFunc(self.time_interval, self.handleTime, None)
        GLUT.glutMainLoop()

    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        """
        GL.glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        GL.glEnable(GL.GL_TEXTURE_2D)
        clientsize = self.getClientSizeTuple()
        self.setupView(clientsize[0], clientsize[1])
        self.init = True

    #methods on this function

    def getClientSizeTuple(self):
        return (GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH),
                GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT))

    def setupView(self, client_width, client_height):
        """This function does the actual work to setup the window so we can 
        draw in it.  Most of its task is going to be sizing the Viewport to
        maintain aspect ratio and sizing the World Window to achieve the 
        maximum possible zoom.
        
        """
        
        world_height = self.world.height 
        world_width = self.world.width  
        
        #The ratio of the width to the height in the client-area
        screenratio = float(client_width) / float(client_height)
        
        ratio = float(world_width) / float(world_height)

        if ratio >= screenratio:
        
            self.viewport_left = 0
            self.viewport_bottom = int((client_height - (client_width / ratio)) / 2)
            self.viewport_width = client_width
            self.viewport_height = int(client_width / ratio)
            
            
        if ratio < screenratio:
        
            self.viewport_left = int((client_width - client_height * ratio) / 2)
            self.viewport_bottom = 0
            self.viewport_width = int(client_height * ratio)
            self.viewport_height = client_height
        
        self.viewport_right = self.viewport_left + self.viewport_width
        self.viewport_top = self.viewport_bottom + self.viewport_height
        
        GL.glViewport(self.viewport_left, 
                      self.viewport_bottom, 
                      self.viewport_width, 
                      self.viewport_height)
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.world.max_left, 
                       self.world.max_right, 
                       self.world.max_bottom, 
                       self.world.max_top)

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)       
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        self.world.render()

        GLUT.glutSwapBuffers()
    
    def onSize(self,width,height):
        """ This function is called when a resize event occurs. The primary
        purpose for this is to readjust the viewport appropriately.
        """
        self.setupView(width, height)

    def handleTime(self, value):
        currentTime = GLUT.glutGet(GLUT.GLUT_ELAPSED_TIME)
        self.world.update(currentTime=currentTime)
        
        self.render()

        GLUT.glutTimerFunc(self.time_interval, self.handleTime, None)
        
