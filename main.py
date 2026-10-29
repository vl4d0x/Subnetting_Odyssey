import os
os.environ.setdefault("PYOPENGL_PLATFORM", "x11")  # en Wayland PyOpenGL elige EGL y falla

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

from characters import mecha7
from scenes import escenarios
from scenes import objetos
from actions import movimiento
from actions import animaciones
from resources import handles as hl
from resources import camera
from resources import audio
from resources import hud

# Tamaño de la ventana
width = 900
height = 680


def init():
    glEnable(GL_DEPTH_TEST)             # prueba de profundidad
    escenarios.cielo()                  # color de cielo y niebla del primer escenario

    # Iluminación: da volumen a las formas
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)              # necesario porque las formas se escalan
    glEnable(GL_COLOR_MATERIAL)         # glColor define el color del material
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.38, 0.38, 0.40, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.90, 0.88, 0.82, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.50, 0.50, 0.50, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.35, 0.35, 0.35, 1.0))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 40.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Cámara (también avanza su suavizado)
    camera.apply_camera()

    # La luz se coloca después de la cámara para que quede fija en el mundo
    glLightfv(GL_LIGHT0, GL_POSITION, (0.5, 0.9, 0.7, 0.0))

    # mover al personaje y revisar choques
    nuevos_choques = movimiento.update()
    if nuevos_choques:
        audio.play_sound("choque")

    animaciones.update()                # avanza los movimientos de Mecha-7
    escenarios.dibujar_escenario()
    objetos.dibujar()

    glPushMatrix()
    glTranslatef(movimiento.pos[0], 0, movimiento.pos[1])
    glRotatef(movimiento.yaw, 0, 1, 0)
    mecha7.dibujar_personaje()
    glPopMatrix()

    hud.dibujar()                       # interfaz 2D encima de la escena

    glutSwapBuffers()


def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w) / float(h), 1.0, 130.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("Mecha-7 - Mecha de Graficación".encode("latin-1"))
    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)
    glutKeyboardFunc(hl.keyboard)
    glutSpecialFunc(hl.special_keys)
    glutKeyboardUpFunc(hl.keyboard_up)
    glutSpecialUpFunc(hl.special_keys_up)
    glutIgnoreKeyRepeat(1)              # solo eventos de presionar / soltar
    glutMouseFunc(camera.mouse)
    glutMouseWheelFunc(camera.mouse_wheel)
    glutMotionFunc(camera.motion)

    audio.init_audio()
    escenarios.cambiar(0)
    movimiento.objetos = objetos.OBJETOS               # sonido del primer escenario
    hl.crear_menu()                     # menú con el clic central del mouse

    glutMainLoop()
    audio.shutdown_audio()


if __name__ == "__main__":
    main()
