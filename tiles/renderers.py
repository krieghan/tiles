import math

from OpenGL import GL

def draw_circle(radius, number_of_triangles):
    GL.glBegin(GL.GL_TRIANGLE_FAN)
    twice_pi = 2.0 * math.pi
    GL.glVertex2f(0, 0)

    for i in range(number_of_triangles + 1):
        GL.glVertex2f(
            radius * math.cos(i * twice_pi / number_of_triangles),
            radius * math.sin(i * twice_pi / number_of_triangles))

    GL.glEnd()

def render_player(agent):
    x, y = agent.getPosition()
    color = (0, 0, 1)
    GL.glPushMatrix()
    GL.glTranslate(x, y, 0)
    GL.glColor3f(*color)
    draw_circle(agent.getLength() / 2.0, 20)
    GL.glPopMatrix()
