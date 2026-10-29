# animaciones.py
# Movimientos de Mecha-7. Los movimientos de "encender / apagar" tienen un nivel
# de 0 a 1 que sube y baja poco a poco, así el robot nunca da saltos bruscos.
# Los movimientos de tiempo fijo (salto, giro, saludo, alerta) avanzan solos.

import math

from OpenGL.GLUT import *

from resources import audio


# ============================================================
# CONFIGURACIÓN
# ============================================================

SALTO_DURACION = 0.9        # segundos en el aire
SALTO_ALTURA = 1.2          # altura máxima del salto
GIRO_DURACION = 1.0         # segundos de una vuelta completa
SALUDO_DURACION = 1.6       # segundos que dura el saludo
ALERTA_DURACION = 1.2       # segundos que se ve el "!"
VELOCIDAD_NIVEL = 4.0       # cambio de nivel por segundo

# movimientos que se encienden y apagan (teclas V, Z, X, C, T, K)
MOVIMIENTOS = ["caminar", "brazo_izq", "brazo_der", "agachado", "inclinar", "heroe"]


# ============================================================
# ESTADO
# ============================================================

nivel = {k: 0.0 for k in MOVIMIENTOS}   # nivel actual (0 a 1)
meta = {k: 0.0 for k in MOVIMIENTOS}    # nivel al que queremos llegar

fase = 0.0          # ángulo de las piernas mientras camina
reloj = 0.0         # segundos totales (parpadeo, luz del pecho, inclinación)
salto_t = None      # None = en el suelo
giro_t = None
saludo_t = None
alerta_t = None

_ultimo = None
_paso_previo = 0


# ============================================================
# DISPARADORES (los llaman las teclas)
# ============================================================

def alternar(nombre):
    """Enciende o apaga un movimiento de la lista MOVIMIENTOS."""
    encendido = not meta[nombre]
    meta[nombre] = 1.0 if encendido else 0.0

    if nombre == "heroe" and encendido:
        audio.play_sound("heroe")
    elif nombre != "caminar":
        audio.play_sound("servo")


def brincar():
    global salto_t
    if salto_t is not None:          # ya está en el aire
        return
    salto_t = 0.0
    audio.play_sound("salto")


def girar():
    global giro_t
    if giro_t is None:
        giro_t = 0.0
        audio.play_sound("servo")


def saludar():
    global saludo_t
    if saludo_t is None:
        saludo_t = 0.0
        audio.play_sound("saludo")


def alerta():
    global alerta_t
    alerta_t = 0.0
    audio.play_sound("alerta")


# ============================================================
# VALORES PARA DIBUJAR (los lee characters/mecha7.py)
# ============================================================

def salto_offset():
    """Altura actual del salto (curva de parábola)."""
    if salto_t is None:
        return 0.0
    s = salto_t / SALTO_DURACION
    return 4.0 * SALTO_ALTURA * s * (1.0 - s)


def giro_angulo():
    if giro_t is None:
        return 0.0
    return 360.0 * giro_t / GIRO_DURACION


def inclinacion():
    """Grados de inclinación hacia adelante y atrás (oscila mientras está activa)."""
    return nivel["inclinar"] * math.sin(reloj * 2.5) * 22.0


def saludo_nivel():
    """0 a 1 a 0: sube el brazo derecho para saludar y lo vuelve a bajar."""
    if saludo_t is None:
        return 0.0
    return math.sin(math.pi * saludo_t / SALUDO_DURACION)


def saludo_onda():
    """Movimiento de la mano mientras saluda."""
    if saludo_t is None:
        return 0.0
    return math.sin(saludo_t * 14.0) * 25.0


def alerta_activa():
    return alerta_t is not None


# ============================================================
# ACTUALIZAR (una vez por cuadro)
# ============================================================

def update():
    global fase, reloj, salto_t, giro_t, saludo_t, alerta_t
    global _ultimo, _paso_previo

    ahora = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    if _ultimo is None:
        _ultimo = ahora
    dt = min(ahora - _ultimo, 0.1)
    _ultimo = ahora
    reloj += dt

    # niveles suaves: se acercan a su meta sin saltos bruscos
    paso = VELOCIDAD_NIVEL * dt
    for clave in nivel:
        dif = meta[clave] - nivel[clave]
        nivel[clave] += max(-paso, min(paso, dif))

    # caminar: las piernas avanzan y cada medio paso suena un "paso"
    if nivel["caminar"] > 0.5:
        fase += dt * 9.0
        pasos = int(fase / math.pi)
        if pasos != _paso_previo:
            _paso_previo = pasos
            audio.play_sound("paso")
    else:
        _paso_previo = int(fase / math.pi)

    if salto_t is not None:
        salto_t += dt
        if salto_t >= SALTO_DURACION:
            salto_t = None

    if giro_t is not None:
        giro_t += dt
        if giro_t >= GIRO_DURACION:
            giro_t = None

    if saludo_t is not None:
        saludo_t += dt
        if saludo_t >= SALUDO_DURACION:
            saludo_t = None

    if alerta_t is not None:
        alerta_t += dt
        if alerta_t >= ALERTA_DURACION:
            alerta_t = None
