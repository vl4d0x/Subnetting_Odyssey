# hud.py
# Interfaz sobre la ventana 3D: estado actual, instrucciones y "Acerca de".
# Todo se dibuja en 2D (proyección ortogonal) encima de la escena, sin ventanas extra.

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from actions import expresiones
from actions import movimiento
from actions import state
from scenes import escenarios
from resources.info import (AUTOR, INSTITUCION, MATERIA, NOMBRE_PERSONAJE,
                            NUMERO_CONTROL, PERIODO, PROFESOR)

mostrar_ayuda = True       # instrucciones (tecla H)
mostrar_acerca = False     # acerca de (tecla I)

AYUDA_IZQ = [
    ("EXPRESIONES", None),
    ("1", "Sonrisa"), ("2", "Guiño"), ("3", "Tristeza"), ("4", "Miedo"),
    ("5", "Enojo"), ("6", "Admiración"), ("7", "Duda"),
    ("", ""),
    ("MOVIMIENTOS", None),
    ("Espacio", "Saltar (propulsores)"),
    ("V", "Caminar (sí / no)"),
    ("Z / X", "Brazo izq. / der. (sí / no)"),
    ("C", "Agacharse (sí / no)"),
    ("T", "Inclinarse (sí / no)"),
    ("K", "Pose de héroe (sí / no)"),
    ("B", "Girar"),
    ("G", "Saludar"),
    ("L", "Alerta (!)"),
]

AYUDA_DER = [
    ("ESCENARIOS", None),
    ("F1 - F7", "Elegir escenario"),
    ("N", "Siguiente escenario"),
    ("", ""),
    ("CÁMARA", None),
    ("Flechas", "Arriba / abajo / izq. / der."),
    ("W A S D", "Mover la cámara"),
    ("Q / E", "Acercar / alejar (zoom)"),
    ("R", "Cámara normal"),
    ("Mouse", "Arrastrar = orbitar"),
    ("Rueda", "Acercar / alejar"),
    ("", ""),
    ("MOVER A MECHA-7", None),
    ("U / J", "Adelante / atrás"),
    ("Y / P", "Izquierda / derecha"),
    ("", ""),
    ("GENERAL", None),
    ("M", "Sonido general ON / OFF"),
    ("0", "Detener sonidos"),
    ("H", "Mostrar / ocultar instrucciones"),
    ("I", "Acerca de"),
    ("Clic central", "Menú rápido"),
    ("ESC", "Salir"),
]


def alternar_ayuda():
    global mostrar_ayuda, mostrar_acerca
    mostrar_ayuda = not mostrar_ayuda
    if mostrar_ayuda:
        mostrar_acerca = False


def alternar_acerca():
    global mostrar_ayuda, mostrar_acerca
    mostrar_acerca = not mostrar_acerca
    if mostrar_acerca:
        mostrar_ayuda = False


def texto(x, y, cadena, fuente=GLUT_BITMAP_HELVETICA_12, color=(1, 1, 1)):
    # sombra oscura para que se lea sobre cualquier fondo
    for dx, dy, col in ((1, -1, (0, 0, 0)), (0, 0, color)):
        glColor3f(*col)
        glRasterPos2f(x + dx, y + dy)
        for c in cadena:
            glutBitmapCharacter(fuente, ord(c))


def panel(x, y, ancho, alto, alfa=0.62):
    glColor4f(0.04, 0.05, 0.10, alfa)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + ancho, y)
    glVertex2f(x + ancho, y + alto)
    glVertex2f(x, y + alto)
    glEnd()


def columna(x, y, filas):
    """Dibuja una columna tecla / acción hacia abajo."""
    for tecla, accion in filas:
        if accion is None:
            texto(x, y, tecla, GLUT_BITMAP_HELVETICA_12, (1.0, 0.85, 0.25))
        elif tecla:
            texto(x, y, tecla, GLUT_BITMAP_HELVETICA_12, (0.55, 0.95, 0.55))
            texto(x + 92, y, accion)
        y -= 17


def dibujar():
    ancho = glutGet(GLUT_WINDOW_WIDTH)
    alto = glutGet(GLUT_WINDOW_HEIGHT)

    # pasar a 2D: proyección ortogonal en píxeles, sin luz ni profundidad
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, ancho, 0, alto)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_FOG)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # ---- barra de estado (arriba) ----
    panel(0, alto - 30, ancho, 30, 0.55)
    sonido = "OFF" if state.muted else "ON"
    texto(10, alto - 20, NOMBRE_PERSONAJE, GLUT_BITMAP_HELVETICA_18, (0.6, 1.0, 0.5))
    choque = ", ".join(sorted(movimiento.choques)) or "ninguno"
    texto(130, alto - 20,
          f"Escenario: {escenarios.nombre()}   |   Expresión: {expresiones.nombre()}"
          f"   |   Choque: {choque}   |   Sonido: {sonido}")

    # ---- pista (abajo) ----
    texto(10, 10, "H instrucciones   I acerca de   M sonido   Clic central = menú",
          GLUT_BITMAP_HELVETICA_12, (0.9, 0.9, 0.9))

    # ---- instrucciones ----
    if mostrar_ayuda:
        pw, ph = 660, 520
        px, py = (ancho - pw) / 2, (alto - ph) / 2 - 10
        panel(px, py, pw, ph, 0.72)
        texto(px + 14, py + ph - 24, "INSTRUCCIONES", GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
        columna(px + 14, py + ph - 52, AYUDA_IZQ)
        columna(px + 340, py + ph - 52, AYUDA_DER)

    # ---- acerca de ----
    if mostrar_acerca:
        pw, ph = 640, 270
        px, py = (ancho - pw) / 2, (alto - ph) / 2
        panel(px, py, pw, ph, 0.78)
        texto(px + 14, py + ph - 26, "ACERCA DE", GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
        lineas = [
            f"Personaje: {NOMBRE_PERSONAJE}, mecha de exploración",
            f"Desarrollado por: {AUTOR}",
            f"Número de control: {NUMERO_CONTROL}",
            f"Materia: {MATERIA}",
            f"Profesor: {PROFESOR}",
            f"Periodo escolar: {PERIODO}",
            f"Institución: {INSTITUCION}",
            "",
            "Hecho con Python, PyOpenGL (GLUT) y pygame.",
            "Presiona I para cerrar.",
        ]
        y = py + ph - 56
        for linea in lineas:
            texto(px + 14, y, linea)
            y -= 20

    # restaurar el estado 3D
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_FOG)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
