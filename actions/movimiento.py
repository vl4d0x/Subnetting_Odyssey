# movimiento.py
# Desplaza a Mecha-7 por el piso y resuelve sus choques con los objetos.
# El personaje se mueve con las teclas U (adelante), J (atrás), Y (izquierda), P (derecha).

import math

from OpenGL.GLUT import *

from actions import animaciones
from actions import colisiones
from resources import camera

VELOCIDAD = 3.0             # unidades por segundo
RADIO = 0.9                 # radio del círculo que ocupa el personaje en el piso
VELOCIDAD_GIRO = 360.0      # grados por segundo al girar hacia donde camina

# posición en el piso (x, z) y ángulo de frente (grados)
pos = [0.0, 0.0]
yaw = 0.0

teclas = set()              # teclas de movimiento mantenidas
choques = set()             # objetos que están tocando al personaje en este cuadro
objetos = []                # lista de objetos con los que puede chocar

_ultimo = None
_caminaba = False


def centrar_camara():
    """La cámara sigue a Mecha-7 (se usa al reiniciar la cámara con R)."""
    camera.TARGET[0] = pos[0]
    camera.TARGET[2] = pos[1]


def resolver():
    """Empuja al personaje fuera de cada objeto con el que choca."""
    choques.clear()
    for obj in objetos:
        for _ in range(2):                       # dos pasadas para casos con dos choques a la vez
            res = colisiones.chocar(pos, RADIO, obj)
            if res is None:
                break
            (nx, nz), prof = res
            pos[0] += nx * prof
            pos[1] += nz * prof
            choques.add(obj["nombre"])


def update():
    global _ultimo, _caminaba, yaw

    ahora = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    if _ultimo is None:
        _ultimo = ahora
    dt = min(ahora - _ultimo, 0.1)
    _ultimo = ahora

    dx = dz = 0.0
    if "adelante" in teclas: dz -= 1.0           # el mundo: adelante es -Z (hacia el castillo)
    if "atras" in teclas: dz += 1.0
    if "izquierda" in teclas: dx -= 1.0
    if "derecha" in teclas: dx += 1.0

    antes = list(choques)
    previo = (pos[0], pos[1])
    caminando = dx != 0 or dz != 0
    if caminando:
        largo = math.hypot(dx, dz)
        dx, dz = dx / largo, dz / largo
        pos[0] += dx * VELOCIDAD * dt
        pos[1] += dz * VELOCIDAD * dt
        # girar hacia donde camina (el frente del personaje es +Z)
        objetivo = math.degrees(math.atan2(dx, dz))
        diferencia = (objetivo - yaw + 180.0) % 360.0 - 180.0
        paso = VELOCIDAD_GIRO * dt
        yaw += max(-paso, min(paso, diferencia))

    # las patas se mueven solo mientras camina
    if caminando and not _caminaba:
        animaciones.meta["caminar"] = 1.0
    elif not caminando and _caminaba:
        animaciones.meta["caminar"] = 0.0
    _caminaba = caminando

    resolver()

    # la cámara se mueve con el personaje, pero conserva el paneo que haya hecho el usuario
    camera.TARGET[0] += pos[0] - previo[0]
    camera.TARGET[2] += pos[1] - previo[1]

    return [c for c in choques if c not in antes]   # objetos con los que empezó a chocar ahora
