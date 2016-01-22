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
    direction = agent.getDirectionDegrees()
    color = (0, 0, 1)
    GL.glPushMatrix()
    GL.glTranslate(x, y, 0)
    GL.glRotatef(direction, 0, 0, 1)
    GL.glColor3f(*color)
    draw_circle(agent.getLength() / 2.0, 20)

    GL.glPopMatrix()

def render_enemy(agent):
    x, y = agent.getPosition()
    direction = agent.getDirectionDegrees()
    color = (1, 0, 0)
    GL.glPushMatrix()
    GL.glTranslate(x, y, 0)
    GL.glRotatef(direction, 0, 0, 1)
    GL.glColor3f(*color)
    draw_circle(agent.getLength() / 2.0, 20)
    GL.glColor3f(1, 1, 1)

    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(0, 0, 0)
    GL.glVertex2f(agent.getLength() * 2.0, 0, 0)
    GL.glEnd()
    GL.glPopMatrix()

def render_obstacle(obstacle):
    x, y = obstacle.getPosition()
    half_width = .5 * obstacle.getWidth()
    half_height = .5 * obstacle.getLength()
    color = (.46, .28, .1)
    GL.glPushMatrix()
    GL.glTranslate(x, y, 0)
    GL.glColor3f(*color)
    GL.glBegin(GL.GL_POLYGON)

    GL.glVertex2f(-half_width, half_height)
    GL.glVertex2f((half_width - 1), half_height)
    GL.glVertex2f((half_width - 1), (-half_height + 1))
    GL.glVertex2f(-half_width, (-half_height + 1))

    GL.glEnd()
    GL.glPopMatrix()
