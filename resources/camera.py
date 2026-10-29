# camera.py
# ============================================================
# CÁMARA ORBITAL EN TERCERA PERSONA
# ============================================================
# La cámara gira alrededor de un punto (el personaje), como en
# un videojuego: el mouse la orbita, la rueda acerca/aleja y
# todos los movimientos se suavizan con inercia.

import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# ============================================================
# OBJETIVO (lo que mira la cámara)
# ============================================================

# Centro aproximado del mecha (el piso está en y = -1)
TARGET = [0.0, 0.9, 0.0]
START_TARGET = tuple(TARGET)    # para reiniciar la cámara


# ============================================================
# VALORES INICIALES
# ============================================================

START_YAW = 20.0         # grados alrededor del personaje
START_PITCH = 15.0       # grados de elevación
START_DISTANCE = 6.0     # distancia al personaje


# ============================================================
# ESTADO DESEADO Y ESTADO ACTUAL (suavizado)
# ============================================================
# Los controles modifican goal_*; update() acerca los valores
# actuales a los deseados, y eso da la sensación de inercia.

goal_yaw = START_YAW
goal_pitch = START_PITCH
goal_distance = START_DISTANCE

yaw = START_YAW
pitch = START_PITCH
distance = START_DISTANCE


# ============================================================
# CONFIGURACIÓN
# ============================================================

mouse_sensitivity = 0.3     # grados por pixel
key_rotate_speed = 90.0     # grados por segundo (teclado)
key_zoom_speed = 8.0        # unidades por segundo (teclado)
move_speed = 6.0            # unidades por segundo al desplazar con WASD
wheel_zoom_step = 0.8       # unidades por click de la rueda

smoothing = 12.0            # mayor = responde más rápido

min_pitch = -30.0
max_pitch = 85.0

min_distance = 3.0
max_distance = 25.0


# ============================================================
# ESTADO DEL MOUSE Y TECLADO
# ============================================================

mouse_down = False

last_mouse_x = 0
last_mouse_y = 0

held_keys = set()           # teclas de cámara mantenidas
last_time = None            # para calcular dt entre cuadros


# ============================================================
# TECLAS DE CÁMARA
# ============================================================

# nombre de la acción para cada tecla
LETTER_KEYS = {
    b'a': "move_left",
    b'd': "move_right",
    b'w': "move_forward",
    b's': "move_back",
    b'q': "zoom_in",
    b'e': "zoom_out",
}

SPECIAL_KEYS = {
    GLUT_KEY_LEFT: "left",
    GLUT_KEY_RIGHT: "right",
    GLUT_KEY_UP: "up",
    GLUT_KEY_DOWN: "down",
    GLUT_KEY_PAGE_UP: "zoom_in",
    GLUT_KEY_PAGE_DOWN: "zoom_out",
}


# ============================================================
# ACTUALIZAR (una vez por cuadro)
# ============================================================

def update():
    """
    Aplica las teclas mantenidas y acerca la cámara actual
    a la deseada. Se llama en cada display().
    """

    global yaw, pitch, distance
    global goal_yaw, goal_pitch, goal_distance
    global last_time

    now = glutGet(GLUT_ELAPSED_TIME) / 1000.0

    if last_time is None:
        last_time = now

    # Limitar dt para que un tirón no mande la cámara muy lejos
    dt = min(now - last_time, 0.1)
    last_time = now

    # ---------- teclas mantenidas ----------
    if "left" in held_keys:
        goal_yaw += key_rotate_speed * dt
    if "right" in held_keys:
        goal_yaw -= key_rotate_speed * dt
    if "up" in held_keys:
        goal_pitch -= key_rotate_speed * dt
    if "down" in held_keys:
        goal_pitch += key_rotate_speed * dt
    if "zoom_in" in held_keys:
        goal_distance -= key_zoom_speed * dt
    if "zoom_out" in held_keys:
        goal_distance += key_zoom_speed * dt

    # ---------- desplazar el punto que mira la cámara (WASD) ----------
    # Se mueve sobre el piso, relativo a hacia dónde mira la cámara
    rad = math.radians(yaw)
    right = (math.cos(rad), -math.sin(rad))
    forward = (-math.sin(rad), -math.cos(rad))

    step = move_speed * dt
    if "move_forward" in held_keys:
        TARGET[0] += forward[0] * step
        TARGET[2] += forward[1] * step
    if "move_back" in held_keys:
        TARGET[0] -= forward[0] * step
        TARGET[2] -= forward[1] * step
    if "move_right" in held_keys:
        TARGET[0] += right[0] * step
        TARGET[2] += right[1] * step
    if "move_left" in held_keys:
        TARGET[0] -= right[0] * step
        TARGET[2] -= right[1] * step

    goal_pitch = max(min_pitch, min(max_pitch, goal_pitch))
    goal_distance = max(min_distance, min(max_distance, goal_distance))

    # ---------- suavizado exponencial (independiente del FPS) ----------
    t = 1.0 - math.exp(-smoothing * dt)

    yaw += (goal_yaw - yaw) * t
    pitch += (goal_pitch - pitch) * t
    distance += (goal_distance - distance) * t


# ============================================================
# APLICAR CÁMARA
# ============================================================

def apply_camera():
    """
    Aplica la transformación de la cámara antes de dibujar.
    Primero se centra el personaje, luego se gira el mundo
    y al final se aleja la cámara.
    """

    update()

    glTranslatef(0.0, 0.0, -distance)

    glRotatef(pitch, 1.0, 0.0, 0.0)

    glRotatef(-yaw, 0.0, 1.0, 0.0)

    glTranslatef(-TARGET[0], -TARGET[1], -TARGET[2])


# ============================================================
# TECLADO
# ============================================================

def handle_key(key):
    """
    Tecla normal presionada. Regresa True si era de la cámara.
    """

    action = LETTER_KEYS.get(key.lower())

    if action is None:
        return False

    held_keys.add(action)

    return True


def handle_key_up(key):
    """
    Tecla normal soltada.
    """

    action = LETTER_KEYS.get(key.lower())

    if action is not None:
        held_keys.discard(action)


def handle_special_keys(key, x, y):
    """
    Flechas y Re Pág / Av Pág presionadas.
    """

    action = SPECIAL_KEYS.get(key)

    if action is not None:
        held_keys.add(action)


def handle_special_keys_up(key, x, y):
    """
    Flechas y Re Pág / Av Pág soltadas.
    """

    action = SPECIAL_KEYS.get(key)

    if action is not None:
        held_keys.discard(action)


# ============================================================
# MOUSE - BOTONES
# ============================================================

def mouse(button, button_state, x, y):
    """
    Clic izquierdo o derecho y arrastrar = orbitar.
    """

    global mouse_down
    global last_mouse_x
    global last_mouse_y

    if button in (GLUT_LEFT_BUTTON, GLUT_RIGHT_BUTTON):

        if button_state == GLUT_DOWN:

            mouse_down = True

            last_mouse_x = x
            last_mouse_y = y

        else:

            mouse_down = False


# ============================================================
# MOUSE - RUEDA
# ============================================================

def mouse_wheel(wheel, direction, x, y):
    """
    Rueda hacia adelante = acercar, hacia atrás = alejar.
    """

    if direction > 0:
        zoom_in()
    else:
        zoom_out()


# ============================================================
# MOVIMIENTO DEL MOUSE
# ============================================================

def motion(x, y):
    """
    Arrastrar con un botón presionado orbita alrededor del personaje.
    """

    global goal_yaw
    global goal_pitch
    global last_mouse_x
    global last_mouse_y

    if not mouse_down:
        return

    dx = x - last_mouse_x
    dy = y - last_mouse_y

    # Arrastrar a la derecha gira la vista a la derecha
    goal_yaw -= dx * mouse_sensitivity

    # Arrastrar hacia abajo mira hacia abajo (la cámara sube)
    goal_pitch += dy * mouse_sensitivity

    goal_pitch = max(min_pitch, min(max_pitch, goal_pitch))

    last_mouse_x = x
    last_mouse_y = y


# ============================================================
# ZOOM
# ============================================================

def zoom_in():

    global goal_distance

    goal_distance = max(min_distance, goal_distance - wheel_zoom_step)


def zoom_out():

    global goal_distance

    goal_distance = min(max_distance, goal_distance + wheel_zoom_step)


# ============================================================
# REINICIAR CÁMARA
# ============================================================

def reset_camera():
    """
    Regresa la cámara a su posición inicial (con animación).
    """

    global goal_yaw, goal_pitch, goal_distance
    global mouse_down

    # Tomar la vuelta más corta hacia el ángulo inicial
    vueltas = round((yaw - START_YAW) / 360.0)

    goal_yaw = START_YAW + 360.0 * vueltas
    goal_pitch = START_PITCH
    goal_distance = START_DISTANCE

    TARGET[:] = START_TARGET

    mouse_down = False
    held_keys.clear()
