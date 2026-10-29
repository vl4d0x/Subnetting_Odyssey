# formas.py
# Figuras básicas de OpenGL reutilizadas por el personaje y los escenarios.
# Todas se dibujan en su propio sistema de coordenadas (glPushMatrix / glPopMatrix).

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

PISO_Y = -1.0           # los pies de Mecha-7 tocan y = -1


def caja(x, y, z, ancho, alto, fondo, color):
    """Prisma con la base apoyada en y."""
    glPushMatrix()
    glTranslatef(x, y + alto / 2, z)
    glScalef(ancho, alto, fondo)
    glColor3f(*color)
    glutSolidCube(1)
    glPopMatrix()


def cilindro(x, y, z, radio, alto, color):
    """Cilindro vertical que nace en (x, y, z) y sube alto unidades."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluCylinder(quad, radio, radio, alto, 16, 1)
    gluDeleteQuadric(quad)
    glPopMatrix()


def cono(x, y, z, radio, alto, color, lados=16):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)
    glutSolidCone(radio, alto, lados, 1)
    glPopMatrix()


def esfera(x, y, z, radio, color, sx=1.0, sy=1.0, sz=1.0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(*color)
    glutSolidSphere(radio, 16, 12)
    glPopMatrix()


def disco(x, z, radio, color, alto=0.0):
    """Círculo plano sobre el piso (o a 'alto' de él)."""
    glPushMatrix()
    glTranslatef(x, PISO_Y + alto, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluDisk(quad, 0, radio, 28, 1)
    gluDeleteQuadric(quad)
    glPopMatrix()


def suelo(color):
    glNormal3f(0, 1, 0)
    disco(0, 0, 70, color, alto=-0.01)


def brillante(dibujar):
    """Dibuja sin luz: para soles, lava, estrellas y luces de neón."""
    glDisable(GL_LIGHTING)
    dibujar()
    glEnable(GL_LIGHTING)
