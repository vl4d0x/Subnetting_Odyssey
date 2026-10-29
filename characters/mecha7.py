# mecha7.py
# Mecha-7: un mecha hecho solo con cubos, cilindros, esferas y conos.
# Cada parte tiene su propio glPushMatrix / glPopMatrix, así las articulaciones
# (caderas, hombros, cuerpo) giran alrededor de su propio punto.

import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from actions import animaciones
from actions import expresiones
from resources.formas import brillante, cilindro, esfera


# ============================================================
# COLORES
# ============================================================

COLOR_CUERPO = (0.62, 0.70, 0.82)     # azul acero
COLOR_CABEZA = (0.78, 0.82, 0.90)
COLOR_ACENTO = (1.00, 0.55, 0.12)     # naranja
COLOR_JUNTA = (0.28, 0.30, 0.36)      # gris oscuro
COLOR_CAPA = (0.90, 0.20, 0.25)       # rojo
COLOR_VISOR = (0.06, 0.08, 0.12)


# ============================================================
# BLOQUE CENTRADO (un cubo estirado)
# ============================================================

def bloque(x, y, z, sx, sy, sz, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(*color)
    glutSolidCube(1)
    glPopMatrix()


# ============================================================
# PIERNAS (cadera -> rodilla -> pie)
# ============================================================

def _pierna(lado, c):
    """lado: -1 izquierda, +1 derecha. c: intensidad de caminar."""
    balanceo = -lado * math.sin(animaciones.fase) * 30.0 * c
    agachado = animaciones.nivel["agachado"]
    tuck = -25.0 if animaciones.salto_offset() > 0.01 else 0.0
    heroe = animaciones.nivel["heroe"]

    glPushMatrix()
    glTranslatef(0.3 * lado, -0.2, 0)                 # cadera
    glRotatef(balanceo - 40.0 * agachado + tuck, 1, 0, 0)
    glRotatef(lado * 12.0 * heroe, 0, 0, 1)           # piernas abiertas (pose de héroe)

    bloque(0, -0.4, 0, 0.34, 0.8, 0.36, COLOR_JUNTA)  # muslo + pantorrilla
    bloque(0, -0.7, 0.06, 0.42, 0.2, 0.56, COLOR_CUERPO)  # pie

    # propulsor: una llama que sale del pie cuando salta
    fuego = animaciones.salto_offset()
    if fuego > 0.01:
        glPushMatrix()
        glTranslatef(0, -0.85, 0)
        glRotatef(180, 1, 0, 0)
        brillante(lambda: _llama(fuego))
        glPopMatrix()

    glPopMatrix()


def _llama(intensidad):
    glColor3f(1.0, 0.8, 0.2)
    glutSolidCone(0.12, 0.2 + intensidad * 0.9, 12, 1)


# ============================================================
# BRAZOS (hombro -> mano)
# ============================================================

def _brazo(lado):
    """lado: -1 izquierdo, +1 derecho."""
    c = animaciones.nivel["caminar"]
    balanceo = lado * math.sin(animaciones.fase) * 25.0 * c   # contrario a la pierna del mismo lado

    heroe = animaciones.nivel["heroe"]
    if lado < 0:
        levantado = animaciones.nivel["brazo_izq"]
        subida = max(levantado * 165.0, heroe * 95.0)
        angulo_z = -subida
        ondeo = 0.0
    else:
        levantado = animaciones.nivel["brazo_der"]
        saludo = animaciones.saludo_nivel()
        subida = max(levantado * 165.0, heroe * 95.0, saludo * 150.0)
        angulo_z = subida
        ondeo = animaciones.saludo_onda()

    glPushMatrix()
    glTranslatef(0.72 * lado, 1.0, 0)                 # hombro
    esfera(0, 0, 0, 0.18, COLOR_JUNTA)
    glRotatef(balanceo, 1, 0, 0)
    glRotatef(angulo_z, 0, 0, 1)
    glRotatef(ondeo, 0, 0, 1)                         # la mano se mueve al saludar
    bloque(0, -0.45, 0, 0.3, 0.9, 0.3, COLOR_CUERPO)  # brazo
    esfera(0, -0.95, 0, 0.17, COLOR_JUNTA)            # mano
    glPopMatrix()


# ============================================================
# TORSO, NÚCLEO Y CAPA
# ============================================================

def _torso():
    bloque(0, 0.5, 0, 1.1, 1.2, 0.7, COLOR_CUERPO)        # pecho
    bloque(0, -0.1, 0, 0.9, 0.2, 0.74, COLOR_JUNTA)       # cintura
    bloque(0, 0.6, 0.36, 0.3, 0.3, 0.05, COLOR_ACENTO)    # placa del pecho

    # núcleo que late como un corazón de energía
    pulso = 0.6 + 0.4 * math.sin(animaciones.reloj * 3.0)
    brillante(lambda: esfera(0, 0.6, 0.4, 0.13, (0.3, 0.9 * pulso + 0.1, 1.0)))


def _capa():
    """Capa roja detrás del cuerpo. Ondea y se abre en la pose de héroe."""
    sway = 8.0 + animaciones.nivel["heroe"] * 18.0 + math.sin(animaciones.reloj * 3.0) * 4.0
    glPushMatrix()
    glTranslatef(0, 1.1, -0.36)
    glRotatef(sway, 1, 0, 0)
    bloque(0, -0.65, 0, 0.85, 1.3, 0.05, COLOR_CAPA)
    glPopMatrix()


# ============================================================
# CABEZA Y VISOR
# ============================================================

def _cabeza():
    glPushMatrix()
    glTranslatef(0, 1.45, 0)
    bloque(0, 0, 0, 0.8, 0.7, 0.7, COLOR_CABEZA)          # cabeza
    bloque(-0.42, 0, 0, 0.1, 0.3, 0.3, COLOR_ACENTO)      # orejas
    bloque(0.42, 0, 0, 0.1, 0.3, 0.3, COLOR_ACENTO)

    # antena con una luz roja que parpadea
    cilindro(0, 0.35, 0, 0.025, 0.35, COLOR_JUNTA)
    if int(animaciones.reloj * 2) % 2 == 0 or animaciones.alerta_activa():
        brillante(lambda: esfera(0, 0.75, 0, 0.06, (1.0, 0.2, 0.2)))

    _visor()
    glPopMatrix()


def _visor():
    glPushMatrix()
    glTranslatef(0, 0.05, 0.36)
    _cara()
    glPopMatrix()


# ============================================================
# CARA: formas 2D sobre el visor (sin luz, para que se vean brillantes)
# ============================================================

def _cara():
    datos = expresiones.datos()
    color = datos["color"]
    izq, der = datos["ojos"]
    parpadea = animaciones.reloj % 3.5 < 0.12      # parpadeo cada 3.5 s

    glPushMatrix()
    glDisable(GL_LIGHTING)
    if datos["tiembla"]:
        glTranslatef(math.sin(animaciones.reloj * 45.0) * 0.01, 0, 0)

    _rect(-0.33, -0.2, 0.33, 0.2, COLOR_VISOR)            # fondo del visor
    glTranslatef(0, 0, 0.002)                             # dibujos un poco delante del fondo

    _ojo(-0.17, izq, color, parpadea, -1)
    _ojo(0.17, der, color, parpadea, 1)

    if datos["cejas"] is not None:
        t_izq, t_der = datos["cejas"]
        _ceja(-0.17, t_izq, color, -1)
        _ceja(0.17, t_der, color, 1)

    _boca(datos["boca"], color)

    if datos["extra"] == "lagrima":
        _poli([(-0.25, -0.06), (-0.2, -0.06), (-0.225, -0.14)], (0.5, 0.8, 1.0))
    elif datos["extra"] == "sudor":
        _poli([(0.27, 0.06), (0.3, 0.06), (0.285, 0.13)], (0.5, 0.85, 1.0))

    glEnable(GL_LIGHTING)
    glPopMatrix()


def _rect(x0, y0, x1, y1, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, 0)
    glVertex3f(x1, y0, 0)
    glVertex3f(x1, y1, 0)
    glVertex3f(x0, y1, 0)
    glEnd()


def _poli(puntos, color):
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for x, y in puntos:
        glVertex3f(x, y, 0)
    glEnd()


def _linea(puntos, grosor, color):
    glColor3f(*color)
    glLineWidth(grosor)
    glBegin(GL_LINE_STRIP)
    for x, y in puntos:
        glVertex3f(x, y, 0)
    glEnd()
    glLineWidth(1.0)


def _ojo(cx, tipo, color, parpadea, lado):
    """Dibuja un ojo. lado: -1 izquierdo, +1 derecho."""
    v0 = 0.04
    if parpadea and tipo in ("abierto", "grande"):
        tipo = "cerrado"

    if tipo == "abierto":
        _rect(cx - 0.05, v0 - 0.08, cx + 0.05, v0 + 0.08, color)
    elif tipo == "grande":
        _rect(cx - 0.07, v0 - 0.11, cx + 0.07, v0 + 0.11, color)
    elif tipo == "cerrado":
        _linea([(cx - 0.07, v0), (cx + 0.07, v0)], 6, color)
    elif tipo == "estrella":
        _rect(cx - 0.03, v0 - 0.03, cx + 0.03, v0 + 0.03, color)
        _linea([(cx - 0.09, v0), (cx + 0.09, v0)], 3, color)
        _linea([(cx, v0 - 0.09), (cx, v0 + 0.09)], 3, color)
    elif tipo == "enojado":
        _ojo_inclinado(cx, v0, color, True, lado)
    elif tipo == "triste":
        _ojo_inclinado(cx, v0, color, False, lado)


def _ojo_inclinado(cx, v0, color, exterior_alto, lado):
    """Ojo trapecio: exterior_alto=True es enojo (el lado de afuera queda más alto)."""
    if (lado < 0) == exterior_alto:
        alto_izq, alto_der = v0 + 0.08, v0 + 0.02
    else:
        alto_izq, alto_der = v0 + 0.02, v0 + 0.08
    _poli([(cx - 0.06, v0 - 0.08), (cx + 0.06, v0 - 0.08),
           (cx + 0.06, alto_der), (cx - 0.06, alto_izq)], color)


def _ceja(cx, t, color, lado):
    """Ceja inclinada: t positivo = el lado de adentro sube."""
    afuera = (cx + lado * 0.09, 0.16 - t)
    adentro = (cx - lado * 0.09, 0.16 + t)
    _linea([afuera, adentro], 4, color)


def _boca(tipo, color):
    if tipo == "sonrisa":
        puntos = [(u, -0.1 + 0.12 * (u / 0.2) ** 2) for u in [-0.2 + 0.05 * i for i in range(9)]]
        _linea(puntos, 5, color)
    elif tipo == "triste":
        puntos = [(u, -0.2 + 0.1 * (1 - (u / 0.2) ** 2)) for u in [-0.2 + 0.05 * i for i in range(9)]]
        _linea(puntos, 5, color)
    elif tipo == "o":
        puntos = [(0.06 * math.cos(a), -0.12 + 0.06 * math.sin(a))
                  for a in [i * 2 * math.pi / 16 for i in range(16)]]
        _poli(puntos, color)
    elif tipo == "enojo":
        _linea([(-0.16, -0.18), (-0.08, -0.12), (0.08, -0.12), (0.16, -0.18)], 6, color)
    elif tipo == "onda":
        _linea([(-0.18, -0.12), (-0.09, -0.06), (0.0, -0.12), (0.09, -0.06), (0.18, -0.12)], 5, color)


# ============================================================
# SÍMBOLO "!" DE ALERTA
# ============================================================

def _alerta():
    if not animaciones.alerta_activa():
        return
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    brillante(lambda: bloque(0, 0.15, 0, 0.14, 0.42, 0.14, (1.0, 0.9, 0.1)))
    brillante(lambda: bloque(0, -0.2, 0, 0.14, 0.14, 0.14, (1.0, 0.9, 0.1)))
    glPopMatrix()


# ============================================================
# DIBUJO COMPLETO
# ============================================================

def dibujar_personaje():
    c = animaciones.nivel["caminar"]
    agachado = animaciones.nivel["agachado"]

    glPushMatrix()
    # subir (salto), agacharse, y girar sobre sí mismo
    glTranslatef(0, animaciones.salto_offset() - 0.19 * agachado, 0)
    glRotatef(animaciones.giro_angulo(), 0, 1, 0)

    _pierna(-1, c)
    _pierna(1, c)

    # la parte de arriba se inclina hacia adelante y atrás desde la cadera
    glPushMatrix()
    glTranslatef(0, -0.2, 0)
    glRotatef(animaciones.inclinacion(), 1, 0, 0)
    glTranslatef(0, 0.2, 0)

    _capa()
    _torso()
    _cabeza()
    _brazo(-1)
    _brazo(1)
    _alerta()

    glPopMatrix()
    glPopMatrix()
