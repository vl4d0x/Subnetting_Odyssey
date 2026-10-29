# colisiones.py
# Algoritmos de colisión en el plano del piso (eje X y Z). Solo matemáticas, sin OpenGL.
# El personaje es un círculo de radio R. Cada objeto tiene una "huella" en el piso:
#   "circulo" -> esfera:  distancia euclidiana
#   "cuadrado" -> caja:   el punto más cercano dentro de un rectángulo (AABB)
#   "rombo"    -> rombo:  métrica del taxi / rombo, |dx| + |dz| <= R
# Cada función devuelve None si no hay choque, o (normal, profundidad) si lo hay.
# La normal apunta hacia el personaje y la profundidad es cuánto hay que empujarlo.

import math

# Margen de contacto: se detecta choque si la separación es menor a 2 cm, y el
# personaje se empuja hasta quedar a 1 cm. Así el choque no parpadea por errores
# de redondeo al empujarlo justo hasta el borde.
MARGEN = 0.02
SEPARACION = MARGEN / 2


def _norma(x, z):
    return math.hypot(x, z)


def _signo(v):
    return 1.0 if v >= 0 else -1.0


# ------------------------------------------------------------
# 1. CÍRCULO contra CÍRCULO (distancia euclidiana)
# ------------------------------------------------------------
def circulo_circulo(p, r, c, rc):
    dx, dz = p[0] - c[0], p[1] - c[1]
    dist = _norma(dx, dz)
    if dist >= r + rc + MARGEN:
        return None
    if dist < 1e-9:
        return (1.0, 0.0), r + rc + SEPARACION
    return (dx / dist, dz / dist), r + rc + SEPARACION - dist


# ------------------------------------------------------------
# 2. CÍRCULO contra RECTÁNGULO (AABB: caja alineada a los ejes)
# ------------------------------------------------------------
def circulo_cuadrado(p, r, c, mitad):
    # el punto de la caja más cercano al centro del personaje (se "sujeta" cada eje)
    qx = max(c[0] - mitad, min(p[0], c[0] + mitad))
    qz = max(c[1] - mitad, min(p[1], c[1] + mitad))
    dx, dz = p[0] - qx, p[1] - qz
    dist = _norma(dx, dz)
    if dist > 1e-9:
        if dist >= r + MARGEN:
            return None
        return (dx / dist, dz / dist), r + SEPARACION - dist

    # el centro quedó dentro de la caja: salir por el lado más cercano
    lx, lz = p[0] - c[0], p[1] - c[1]
    falta_x = mitad - abs(lx)
    falta_z = mitad - abs(lz)
    if falta_x < falta_z:
        return (_signo(lx), 0.0), r + falta_x
    return (0.0, _signo(lz)), r + falta_z


# ------------------------------------------------------------
# 3. CÍRCULO contra ROMBO (métrica del rombo: |dx| + |dz| <= R)
# ------------------------------------------------------------
def _punto_en_segmento(p, a, b):
    """Punto de un segmento a-b más cercano a p."""
    abx, abz = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * abx + (p[1] - a[1]) * abz) / (abx * abx + abz * abz)
    t = max(0.0, min(1.0, t))
    return (a[0] + t * abx, a[1] + t * abz)


def circulo_rombo(p, r, c, R):
    lx, lz = p[0] - c[0], p[1] - c[1]
    metrica = abs(lx) + abs(lz)                 # distancia del taxi (rombo)
    cuarto = (_signo(lx), _signo(lz))           # cuadrante donde está el personaje
    normal_cara = (cuarto[0] / math.sqrt(2), cuarto[1] / math.sqrt(2))

    if metrica < R:                             # el centro está dentro del rombo
        return normal_cara, r + (R - metrica) / math.sqrt(2)

    # fuera: buscar el punto más cercano sobre los 4 lados del rombo
    vertices = [(c[0] + R, c[1]), (c[0], c[1] + R), (c[0] - R, c[1]), (c[0], c[1] - R)]
    mejor = None
    for i in range(4):
        q = _punto_en_segmento(p, vertices[i], vertices[(i + 1) % 4])
        d = _norma(p[0] - q[0], p[1] - q[1])
        if mejor is None or d < mejor[1]:
            mejor = (q, d)
    q, dist = mejor
    if dist >= r + MARGEN:
        return None
    dx, dz = p[0] - q[0], p[1] - q[1]
    if dist < 1e-9:
        return normal_cara, r + SEPARACION
    return (dx / dist, dz / dist), r + SEPARACION - dist


# ------------------------------------------------------------
# Despacho general: un objeto es un diccionario con "forma" y sus datos
# ------------------------------------------------------------
def chocar(p, r, objeto):
    forma = objeto["forma"]
    if forma == "circulo":
        return circulo_circulo(p, r, objeto["centro"], objeto["radio"])
    if forma == "cuadrado":
        return circulo_cuadrado(p, r, objeto["centro"], objeto["mitad"])
    if forma == "rombo":
        return circulo_rombo(p, r, objeto["centro"], objeto["radio"])
    return None
