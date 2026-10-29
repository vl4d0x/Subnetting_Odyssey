# objetos.py
# Tres objetos con los que choca Mecha-7. Cada uno usa un algoritmo distinto
# (ver actions/colisiones.py). Se dibujan encima de cualquier escenario.

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from actions import movimiento
from resources.formas import PISO_Y, caja, esfera

BLANCO = (1.0, 1.0, 1.0)

# Cada objeto: forma en el piso (para colisionar) y sus datos de dibujo.
#   circulo  -> esfera de radio "radio"
#   cuadrado -> caja de lado 2 * "mitad"
#   rombo    -> octaedro con vértices a distancia "radio" de su centro
OBJETOS = [
    dict(nombre="Esfera", forma="circulo", centro=(3.2, -2.2), radio=1.0,
         color=(1.0, 0.35, 0.75)),
    dict(nombre="Caja", forma="cuadrado", centro=(-3.0, -3.0), mitad=1.0,
         color=(0.55, 1.0, 0.35)),
    dict(nombre="Rombo", forma="rombo", centro=(2.6, 2.6), radio=1.3,
         color=(0.30, 0.85, 1.0)),
]


def _color(obj):
    """Se ilumina (se vuelve blanco) mientras el personaje lo toca."""
    if obj["nombre"] in movimiento.choques:
        return BLANCO
    return obj["color"]


def _rombo(cx, cy, cz, R, color):
    """Octaedro: 8 caras triangulares con vértices en los ejes."""
    glColor3f(*color)
    glBegin(GL_TRIANGLES)
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                # cada cara toca un vértice en cada eje; la normal apunta hacia afuera
                a = (cx + sx * R, cy, cz)
                b = (cx, cy + sy * R, cz)
                c = (cx, cy, cz + sz * R)
                glNormal3f(sx, sy, sz)
                for v in (a, b, c):
                    glVertex3f(*v)
    glEnd()


def dibujar():
    # esfera: su centro queda a radio sobre el piso
    for obj in OBJETOS:
        cx, cz = obj["centro"]
        color = _color(obj)
        if obj["forma"] == "circulo":
            r = obj["radio"]
            esfera(cx, PISO_Y + r, cz, r, color)
        elif obj["forma"] == "cuadrado":
            m = obj["mitad"]
            caja(cx, PISO_Y, cz, 2 * m, 2 * m, 2 * m, color)
        elif obj["forma"] == "rombo":
            R = obj["radio"]
            _rombo(cx, PISO_Y + R, cz, R, color)
