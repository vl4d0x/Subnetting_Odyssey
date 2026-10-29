from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from resources import audio
from resources import camera
from resources import hud
from actions import animaciones
from actions import expresiones
from actions import movimiento
from scenes import escenarios

# ------------------------------------------------------------
# ACCIONES: cada una se puede lanzar con una tecla o con el menú
# ------------------------------------------------------------
ACCIONES = {
    # expresiones (teclas 1 a 7)
    "sonrisa":    lambda: expresiones.poner("sonrisa"),
    "guino":      lambda: expresiones.poner("guino"),
    "tristeza":   lambda: expresiones.poner("tristeza"),
    "miedo":      lambda: expresiones.poner("miedo"),
    "enojo":      lambda: expresiones.poner("enojo"),
    "admiracion": lambda: expresiones.poner("admiracion"),
    "duda":       lambda: expresiones.poner("duda"),
    # movimientos
    "brincar":   animaciones.brincar,
    "caminar":   lambda: animaciones.alternar("caminar"),
    "brazo_izq": lambda: animaciones.alternar("brazo_izq"),
    "brazo_der": lambda: animaciones.alternar("brazo_der"),
    "agacharse": lambda: animaciones.alternar("agachado"),
    "inclinar":  lambda: animaciones.alternar("inclinar"),
    "heroe":     lambda: animaciones.alternar("heroe"),
    "girar":     animaciones.girar,
    "saludar":   animaciones.saludar,
    "alerta":    animaciones.alerta,
    # escenarios (teclas F1 a F7)
    "esc1": lambda: escenarios.cambiar(0),
    "esc2": lambda: escenarios.cambiar(1),
    "esc3": lambda: escenarios.cambiar(2),
    "esc4": lambda: escenarios.cambiar(3),
    "esc5": lambda: escenarios.cambiar(4),
    "esc6": lambda: escenarios.cambiar(5),
    "esc7": lambda: escenarios.cambiar(6),
    "esc_sig": escenarios.siguiente,
    # general
    "mute":          audio.toggle_mute,
    "silencio":      audio.stop_all_sounds,
    "ayuda":         hud.alternar_ayuda,
    "acerca":        hud.alternar_acerca,
    "camara_normal": lambda: (camera.reset_camera(), movimiento.centrar_camara()),
}

# teclas que mueven a Mecha-7 (se mantienen presionadas)
TECLAS_MOVER = {
    b'u': "adelante", b'j': "atras", b'y': "izquierda", b'p': "derecha",
}

# tecla -> acción
TECLAS = {
    b'1': "sonrisa", b'2': "guino", b'3': "tristeza", b'4': "miedo",
    b'5': "enojo", b'6': "admiracion", b'7': "duda",
    b' ': "brincar", b'v': "caminar", b'z': "brazo_izq", b'x': "brazo_der",
    b'c': "agacharse", b't': "inclinar", b'k': "heroe", b'b': "girar",
    b'g': "saludar", b'l': "alerta",
    b'n': "esc_sig",
    b'm': "mute", b'0': "silencio", b'h': "ayuda", b'i': "acerca",
    b'r': "camara_normal",
}

# teclas especiales F1..F7 -> escenario
TECLAS_F = {
    GLUT_KEY_F1: "esc1", GLUT_KEY_F2: "esc2", GLUT_KEY_F3: "esc3", GLUT_KEY_F4: "esc4",
    GLUT_KEY_F5: "esc5", GLUT_KEY_F6: "esc6", GLUT_KEY_F7: "esc7",
}

# entradas del menú (clic central): (texto, acción)
MENU = [
    ("Escenario: Taller de Chatarra", "esc1"),
    ("Escenario: Ciudad Neón", "esc2"),
    ("Escenario: Desierto Solar", "esc3"),
    ("Escenario: Volcán Ardiente", "esc4"),
    ("Escenario: Glaciar", "esc5"),
    ("Escenario: Bosque de Cristal", "esc6"),
    ("Escenario: Estación Lunar", "esc7"),
    ("Expresión: Sonrisa", "sonrisa"),
    ("Expresión: Guiño", "guino"),
    ("Expresión: Tristeza", "tristeza"),
    ("Expresión: Miedo", "miedo"),
    ("Expresión: Enojo", "enojo"),
    ("Expresión: Admiración", "admiracion"),
    ("Expresión: Duda", "duda"),
    ("Saltar", "brincar"),
    ("Caminar (sí / no)", "caminar"),
    ("Pose de héroe", "heroe"),
    ("Saludar", "saludar"),
    ("Alerta (!)", "alerta"),
    ("Sonido ON / OFF", "mute"),
    ("Instrucciones", "ayuda"),
    ("Acerca de", "acerca"),
]


def menu_seleccion(valor):
    ACCIONES[MENU[valor][1]]()
    return 0


def crear_menu():
    """Menú emergente con el botón central del mouse."""
    glutCreateMenu(menu_seleccion)
    for i, (texto, _) in enumerate(MENU):
        glutAddMenuEntry(texto.encode("latin-1"), i)
    glutAttachMenu(GLUT_MIDDLE_BUTTON)


def keyboard(key, x, y):
    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()
        return

    if camera.handle_key(key):  # W A S D / Q / E
        return

    if key.lower() in TECLAS_MOVER:
        movimiento.teclas.add(TECLAS_MOVER[key.lower()])
        return

    accion = TECLAS.get(key.lower())
    if accion:
        ACCIONES[accion]()


def keyboard_up(key, x, y):
    camera.handle_key_up(key)
    if key.lower() in TECLAS_MOVER:
        movimiento.teclas.discard(TECLAS_MOVER[key.lower()])


def special_keys(key, x, y):
    accion = TECLAS_F.get(key)
    if accion:
        ACCIONES[accion]()
    else:
        camera.handle_special_keys(key, x, y)


def special_keys_up(key, x, y):
    camera.handle_special_keys_up(key, x, y)
