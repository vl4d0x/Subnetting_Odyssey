# expresiones.py
# Catálogo de expresiones de Mecha-7. Se dibujan en su visor (la pantalla de la cara).
# characters/mecha7.py lee estos datos para dibujar ojos, cejas y boca.

from resources import audio


# Cada expresión describe la cara:
#   nombre  -> texto que se muestra en pantalla
#   sonido  -> efecto que suena al activarla
#   ojos    -> (ojo izquierdo, ojo derecho): "abierto", "grande", "cerrado",
#              "estrella", "enojado" o "triste"
#   cejas   -> inclinación de cada ceja (positiva = el lado de adentro sube) o None
#   boca    -> "sonrisa", "triste", "o", "enojo" u "onda"
#   color   -> color de los ojos y la boca (RGB)
#   extra   -> "lagrima", "sudor" o None
#   tiembla -> True si la cara vibra (miedo)
EXPRESIONES = {
    "sonrisa": dict(nombre="Sonrisa", sonido="sonrisa", ojos=("abierto", "abierto"),
                    cejas=None, boca="sonrisa", color=(0.35, 0.95, 1.0), extra=None, tiembla=False),
    "guino": dict(nombre="Guiño", sonido="guino", ojos=("abierto", "cerrado"),
                  cejas=None, boca="sonrisa", color=(0.35, 0.95, 1.0), extra=None, tiembla=False),
    "tristeza": dict(nombre="Tristeza", sonido="tristeza", ojos=("triste", "triste"),
                     cejas=(0.05, 0.05), boca="triste", color=(0.40, 0.60, 1.0),
                     extra="lagrima", tiembla=False),
    "miedo": dict(nombre="Miedo", sonido="miedo", ojos=("grande", "grande"),
                  cejas=(0.06, 0.06), boca="o", color=(1.0, 0.90, 0.25),
                  extra="sudor", tiembla=True),
    "enojo": dict(nombre="Enojo", sonido="enojo", ojos=("enojado", "enojado"),
                  cejas=(-0.06, -0.06), boca="enojo", color=(1.0, 0.25, 0.20),
                  extra=None, tiembla=False),
    "admiracion": dict(nombre="Admiración", sonido="admiracion", ojos=("estrella", "estrella"),
                       cejas=(0.03, 0.03), boca="o", color=(0.55, 1.0, 0.55),
                       extra=None, tiembla=False),
    "duda": dict(nombre="Duda", sonido="duda", ojos=("abierto", "grande"),
                 cejas=(0.0, 0.07), boca="onda", color=(1.0, 0.62, 0.20),
                 extra=None, tiembla=False),
}

# orden de las teclas 1 a 7
ORDEN = ["sonrisa", "guino", "tristeza", "miedo", "enojo", "admiracion", "duda"]

actual = "sonrisa"


def poner(clave):
    """Activa una expresión y reproduce su sonido."""
    global actual
    actual = clave
    audio.play_sound(EXPRESIONES[clave]["sonido"])


def datos():
    return EXPRESIONES[actual]


def nombre():
    return EXPRESIONES[actual]["nombre"]
