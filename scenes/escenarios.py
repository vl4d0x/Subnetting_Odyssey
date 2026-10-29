# escenarios.py
# Siete escenarios diseñados solo con figuras básicas (cubos, cilindros, esferas,
# conos y discos). No usan imágenes. Cada uno tiene su cielo, su niebla y su
# sonido general (ambiente en bucle).

import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from actions import animaciones
from resources import audio
from resources.formas import PISO_Y, brillante, caja, cilindro, cono, disco, esfera, suelo


# ============================================================
# AYUDAS
# ============================================================

def tubo_x(x, y, z, radio, largo, color):
    """Cilindro horizontal que empieza en x y avanza hacia +x."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(90, 0, 1, 0)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluCylinder(quad, radio, radio, largo, 14, 1)
    gluDeleteQuadric(quad)
    glPopMatrix()


def _brillo_sinusoidal(i, velocidad=1.5):
    return 0.5 + 0.5 * math.sin(animaciones.reloj * velocidad + i)


# ============================================================
# 1. TALLER DE CHATARRA
# ============================================================

def taller():
    cajas = [(-6, -5, 3, (0.95, 0.55, 0.15)), (-7.6, -4, 2, (0.85, 0.25, 0.15)),
             (6, -6, 4, (0.95, 0.80, 0.20)), (7.4, -4.4, 2, (0.30, 0.60, 0.90))]
    for x, z, alto, color in cajas:
        for k in range(alto):
            caja(x, PISO_Y + k * 1.0, z, 1.1, 1.0, 1.1, color)

    # tuberías en el techo
    for y, z, color in [(3.6, -10, (0.50, 0.50, 0.56)), (4.4, -14, (0.85, 0.45, 0.20))]:
        tubo_x(-14, y, z, 0.22, 28, color)

    # engranajes que giran (cuanto más grande, más lento)
    engranajes = [(-4.5, 1.6, -13, 1.7, (0.95, 0.75, 0.20), 40),
                  (3.5, 2.2, -14, 2.3, (0.90, 0.40, 0.20), -30),
                  (9.5, 1.2, -11, 1.3, (0.60, 0.80, 0.90), 60)]
    for x, y, z, radio, color, velocidad in engranajes:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(animaciones.reloj * velocidad, 0, 0, 1)
        glColor3f(*color)
        glutSolidTorus(0.25, radio, 8, 14)
        for k in range(6):                       # dientes
            glPushMatrix()
            glRotatef(k * 60, 0, 0, 1)
            caja(0, radio - 0.1, 0, 0.25, 0.35, 0.25, color)
            glPopMatrix()
        glPopMatrix()

    # lámparas colgadas del techo
    for x, z in [(-3, -3), (3, -2), (0, -8)]:
        cilindro(x, 3.2, z, 0.02, 1.2, (0.2, 0.2, 0.2))
        brillante(lambda x=x, z=z: esfera(x, 2.9, z, 0.22, (1.0, 0.95, 0.5)))


# ============================================================
# 2. CIUDAD NEÓN
# ============================================================

def ciudad_neon():
    # calles de neón
    for z, color in [(-8, (1.0, 0.2, 0.8)), (-16, (0.2, 1.0, 1.0)), (-24, (1.0, 0.9, 0.2))]:
        brillante(lambda z=z, color=color: caja(0, PISO_Y + 0.01, z, 70, 0.02, 0.15, color))

    edificios = [(-9, -10, 2.5, 7, (0.9, 0.2, 0.7)), (-4, -18, 1.8, 11, (0.2, 0.9, 1.0)),
                 (6, -12, 2.2, 9, (1.0, 0.8, 0.2)), (11, -20, 3.0, 14, (0.6, 0.3, 1.0)),
                 (-13, -24, 3.2, 13, (0.3, 1.0, 0.5)), (2, -26, 2.6, 16, (1.0, 0.4, 0.4)),
                 (-18, -12, 2.4, 8, (0.4, 0.6, 1.0)), (16, -9, 2.0, 6, (1.0, 0.5, 0.8))]
    for x, z, ancho, alto, color in edificios:
        caja(x, PISO_Y, z, ancho, alto, ancho, (0.14, 0.12, 0.24))
        # ventanas que brillan
        for k in range(int(alto)):
            for c in (-0.5, 0.5):
                brillante(lambda x=x, k=k, c=c, z=z, ancho=ancho:
                          caja(x + c * ancho * 0.5, PISO_Y + 0.6 + k, z + ancho / 2 + 0.01,
                               ancho * 0.3, 0.35, 0.02, color))

    # letrero gigante que cambia de color
    pulso = _brillo_sinusoidal(0, 2.0)
    brillante(lambda: caja(0, 4.5, -34, 9, 2.4, 0.3, (pulso, 0.3, 1.0 - pulso * 0.5)))


# ============================================================
# 3. DESIERTO SOLAR
# ============================================================

def desierto():
    # dunas aplastadas
    for x, z, radio in [(-14, -14, 6), (2, -20, 9), (16, -16, 7), (-4, -36, 12), (18, -34, 10)]:
        esfera(x, PISO_Y, z, radio, (0.95, 0.82, 0.50), 1.0, 0.22, 1.0)

    # cactus con brazo
    for x, z, alto in [(-6, -7, 2.4), (7, -9, 3.0), (-10, -22, 3.6), (12, -26, 2.8)]:
        cilindro(x, PISO_Y, z, 0.28, alto, (0.25, 0.62, 0.28))
        tubo_x(x, PISO_Y + alto * 0.5, z, 0.14, 0.5, (0.25, 0.62, 0.28))
        cilindro(x + 0.5, PISO_Y + alto * 0.5, z, 0.14, 0.7, (0.25, 0.62, 0.28))

    # pirámides de colores
    glPushMatrix()
    glRotatef(45, 0, 1, 0)
    cono(-16, PISO_Y, -26, 3.2, 3.6, (0.92, 0.62, 0.26), 4)
    cono(20, PISO_Y, -24, 2.6, 3.0, (0.85, 0.50, 0.22), 4)
    glPopMatrix()

    # el sol
    brillante(lambda: esfera(-8, 9, -30, 2.6, (1.0, 0.95, 0.35)))


# ============================================================
# 4. VOLCÁN
# ============================================================

def volcan():
    # el volcán con su cráter de lava
    cono(0, PISO_Y, -26, 9, 11, (0.30, 0.14, 0.11), 16)
    brillante(lambda: disco(0, -26, 3.0, (1.0, 0.45, 0.05), alto=11.0))

    # ríos de lava que bajan del volcán
    for k in range(4):
        brillo = _brillo_sinusoidal(k, 2.0)
        x = -7 + k * 4.5
        brillante(lambda x=x, brillo=brillo, k=k:
                  caja(x, PISO_Y + 0.01, -14 - k * 2, 1.2, 0.02, 14,
                       (1.0, 0.35 + 0.25 * brillo, 0.05)))

    # rocas oscuras
    for x, z, radio in [(-12, -8, 1.6), (10, -6, 1.3), (-15, -18, 2.2), (14, -16, 1.8)]:
        esfera(x, PISO_Y, z, radio, (0.22, 0.20, 0.20), 1.0, 0.6, 1.0)

    # humo que sube del cráter
    for k in range(6):
        altura = PISO_Y + 12 + ((animaciones.reloj * 1.2 + k) % 6)
        esfera(math.sin(k * 2.0) * 0.8, altura, -26, 1.0 + 0.15 * k, (0.52, 0.46, 0.46))


# ============================================================
# 5. GLACIAR
# ============================================================

def glaciar():
    # cristales de hielo
    for x, z, alto in [(-8, -8, 4), (9, -10, 5.5), (-14, -20, 7), (6, -22, 6), (-2, -28, 8)]:
        cono(x, PISO_Y, z, 1.4, alto, (0.62, 0.88, 1.0), 6)

    # pinos nevados
    for x, z in [(-11, -14), (-6, -26), (10, -18), (15, -26), (0, -34)]:
        cono(x, PISO_Y, z, 1.6, 3.2, (0.30, 0.62, 0.55), 12)
        cono(x, PISO_Y + 2.2, z, 0.9, 1.4, (0.98, 1.0, 1.0), 12)

    # muñeco de nieve
    esfera(-3.5, PISO_Y, -9, 0.8, (0.98, 0.98, 1.0))
    esfera(-3.5, PISO_Y + 1.1, -9, 0.55, (0.98, 0.98, 1.0))
    cono(-3.5, PISO_Y + 1.2, -8.2, 0.12, 0.6, (1.0, 0.5, 0.1), 8)

    # aurora boreal al fondo
    for k in range(8):
        alto = 10 + 3 * math.sin(animaciones.reloj * 0.8 + k)
        color = (0.3, 1.0, 0.6) if k % 2 == 0 else (0.7, 0.4, 1.0)
        brillante(lambda k=k, alto=alto, color=color:
                  caja(-30 + k * 8, PISO_Y, -55, 2.0, alto, 0.3, color))


# ============================================================
# 6. BOSQUE DE CRISTAL
# ============================================================

def bosque_cristal():
    # árboles de cristal
    for x, z in [(-9, -7), (8, -9), (-14, -16), (13, -18), (-5, -24), (5, -28), (-17, -28)]:
        cilindro(x, PISO_Y, z, 0.22, 2.4, (0.55, 0.85, 0.90))
        cono(x, PISO_Y + 2.0, z, 1.4, 2.4, (0.90, 0.30, 0.95), 6)
        cono(x, PISO_Y + 3.0, z, 0.95, 2.0, (0.20, 0.95, 0.80), 6)

    # hongos de colores
    for x, z in [(-4, -5), (4, -6), (-11, -11), (10, -14)]:
        cilindro(x, PISO_Y, z, 0.15, 0.7, (0.95, 0.92, 0.85))
        cono(x, PISO_Y + 0.7, z, 0.6, 0.4, (1.0, 0.50, 0.80), 10)

    # luciérnagas que flotan
    for i in range(9):
        x = math.cos(i * 0.9) * (6 + i % 3 * 3)
        z = -4 - math.sin(i * 0.9) * (6 + i % 3 * 3)
        y = PISO_Y + 2.5 + math.sin(animaciones.reloj * 1.5 + i) * 0.5
        brillante(lambda x=x, y=y, z=z: esfera(x, y, z, 0.2, (1.0, 0.95, 0.4)))


# ============================================================
# 7. ESTACIÓN LUNAR
# ============================================================

_ESTRELLAS = None


def _estrellas():
    """Puntos fijos en una cúpula (se calculan una sola vez)."""
    global _ESTRELLAS
    if _ESTRELLAS is None:
        rnd = random.Random(12)
        _ESTRELLAS = []
        for _ in range(160):
            a = rnd.uniform(0, 2 * math.pi)
            h = rnd.uniform(0.05, 1.0)
            r = 80.0
            _ESTRELLAS.append((math.cos(a) * r * math.sqrt(1 - h * h), h * r, math.sin(a) * r * math.sqrt(1 - h * h)))
    return _ESTRELLAS


def luna():
    # cráteres
    for x, z, radio in [(-10, -10, 3), (8, -12, 2), (-16, -24, 4), (12, -26, 3.2), (0, -32, 5)]:
        disco(x, z, radio, (0.42, 0.42, 0.48), alto=0.01)

    # estrellas
    def puntos():
        glPointSize(2.5)
        glBegin(GL_POINTS)
        for x, y, z in _estrellas():
            glColor3f(1.0, 1.0, 0.9)
            glVertex3f(x, y, z)
        glEnd()
        glPointSize(1.0)
    brillante(puntos)

    # planeta azul con anillo
    glPushMatrix()
    glTranslatef(30, 18, -60)
    esfera(0, 0, 0, 9, (0.25, 0.50, 1.0))
    glRotatef(70, 1, 0, 0)
    glColor3f(0.8, 0.85, 1.0)
    glutSolidTorus(0.6, 14, 10, 40)
    glPopMatrix()

    # torres de la estación con luces que parpadean
    for x, z in [(-7, -14), (7, -16)]:
        cilindro(x, PISO_Y, z, 0.2, 4.0, (0.75, 0.75, 0.80))
        luz = 1.0 if int(animaciones.reloj * 2) % 2 == 0 else 0.2
        brillante(lambda x=x, z=z, luz=luz: esfera(x, PISO_Y + 4.1, z, 0.18, (1.0 * luz, 0.2, 0.2)))


# ============================================================
# CATÁLOGO DE ESCENARIOS
# ============================================================
# nombre, cielo (RGB), niebla (inicio, fin), color del piso, ambiente (sonido general)
ESCENARIOS = [
    dict(nombre="Taller de Chatarra", cielo=(0.98, 0.62, 0.30), niebla=(30, 80),
         piso=(0.42, 0.40, 0.38), musica="amb_taller", dibujar=taller),
    dict(nombre="Ciudad Neón", cielo=(0.08, 0.04, 0.20), niebla=(14, 60),
         piso=(0.12, 0.09, 0.20), musica="amb_neon", dibujar=ciudad_neon),
    dict(nombre="Desierto Solar", cielo=(1.0, 0.82, 0.45), niebla=(40, 110),
         piso=(0.93, 0.75, 0.42), musica="amb_desierto", dibujar=desierto),
    dict(nombre="Volcán Ardiente", cielo=(0.30, 0.06, 0.04), niebla=(15, 70),
         piso=(0.20, 0.12, 0.11), musica="amb_volcan", dibujar=volcan),
    dict(nombre="Glaciar", cielo=(0.70, 0.88, 1.0), niebla=(20, 70),
         piso=(0.95, 0.98, 1.0), musica="amb_glaciar", dibujar=glaciar),
    dict(nombre="Bosque de Cristal", cielo=(0.04, 0.20, 0.26), niebla=(10, 45),
         piso=(0.10, 0.34, 0.36), musica="amb_cristal", dibujar=bosque_cristal),
    dict(nombre="Estación Lunar", cielo=(0.02, 0.02, 0.07), niebla=(40, 120),
         piso=(0.52, 0.52, 0.58), musica="amb_luna", dibujar=luna),
]

actual = 0


def nombre():
    return ESCENARIOS[actual]["nombre"]


def cielo():
    """Color del cielo y niebla del escenario actual."""
    esc = ESCENARIOS[actual]
    glClearColor(*esc["cielo"], 1.0)
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, (*esc["cielo"], 1.0))
    glFogf(GL_FOG_START, esc["niebla"][0])
    glFogf(GL_FOG_END, esc["niebla"][1])


def cambiar(indice):
    """Cambia de escenario y empieza su sonido general."""
    global actual
    actual = indice % len(ESCENARIOS)
    cielo()
    audio.play_ambient(ESCENARIOS[actual]["musica"])


def siguiente():
    cambiar(actual + 1)


def dibujar_escenario():
    esc = ESCENARIOS[actual]
    suelo(esc["piso"])
    esc["dibujar"]()
