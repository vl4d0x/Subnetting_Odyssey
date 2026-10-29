# generar_sonidos.py
# Crea todos los sonidos del proyecto como archivos WAV en utils/sonidos/.
# Se ejecuta una sola vez:  python utils/generar_sonidos.py
# Los sonidos se sintetizan con funciones matemáticas (senos, cuadrados, ruido),
# así no dependemos de archivos ajenos.

import math
import os
import random
import struct
import wave

RATE = 22050
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos")


# ============================================================
# BLOQUES BÁSICOS
# ============================================================

def envolvente(i, total, ataque=0.01, caida=0.15):
    """Sube rápido al inicio y se apaga al final."""
    t = i / RATE
    dur = total / RATE
    sube = min(1.0, t / ataque) if ataque > 0 else 1.0
    baja = min(1.0, (dur - t) / caida) if caida > 0 else 1.0
    return max(0.0, sube * baja)


def onda(tipo, fase):
    if tipo == "seno":
        return math.sin(fase)
    if tipo == "cuadrado":
        return 1.0 if math.sin(fase) >= 0 else -1.0
    if tipo == "diente":                       # sierra: suena a motor
        return 2.0 * ((fase / (2 * math.pi)) % 1.0) - 1.0
    return 0.0


def tono(frecuencia, dur, tipo="seno", volumen=0.5, ataque=0.01, caida=0.15, vibrato=0.0):
    """Tono con frecuencia fija o función frecuencia(t)."""
    n = int(dur * RATE)
    salida = []
    fase = 0.0
    for i in range(n):
        t = i / RATE
        f = frecuencia(t) if callable(frecuencia) else frecuencia
        if vibrato:
            f *= 1.0 + vibrato * math.sin(2 * math.pi * 6 * t)
        fase += 2 * math.pi * f / RATE
        salida.append(volumen * envolvente(i, n, ataque, caida) * onda(tipo, fase))
    return salida


def silencio(dur):
    return [0.0] * int(dur * RATE)


def mezclar(*pistas):
    largo = max(len(p) for p in pistas)
    salida = [0.0] * largo
    for p in pistas:
        for i, v in enumerate(p):
            salida[i] += v
    return salida


def concatenar(*pistas):
    salida = []
    for p in pistas:
        salida.extend(p)
    return salida


def ruido_suave(n, paso=0.05, seed=1):
    """Ruido filtrado (pasa bajas simple): suena a viento o rugido."""
    rnd = random.Random(seed)
    salida = []
    valor = 0.0
    for _ in range(n):
        valor += paso * (rnd.uniform(-1, 1) - valor)
        salida.append(valor * 4.0)
    return salida


def guardar(nombre, muestras, volumen_final=0.8):
    pico = max(1e-6, max(abs(v) for v in muestras))
    escala = volumen_final / pico
    ruta = os.path.join(DESTINO, nombre + ".wav")
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        datos = b"".join(struct.pack("<h", int(max(-1, min(1, v * escala)) * 32767)) for v in muestras)
        w.writeframes(datos)
    print("creado", ruta)


def loop(muestras, fundido=0.5):
    """Vuelve el sonido continuo: el final se funde con el inicio."""
    f = int(fundido * RATE)
    n = len(muestras)
    salida = list(muestras[: n - f])
    for i in range(f):
        a = i / f
        salida[i] = muestras[i] * a + muestras[n - f + i] * (1 - a)
    return salida


# ============================================================
# EFECTOS (un sonido por expresión y por movimiento)
# ============================================================

def efectos():
    # salto: barrido hacia arriba, como un propulsor
    guardar("salto", tono(lambda t: 220 + 900 * t / 0.35, 0.35, "diente", 0.5, 0.01, 0.2))

    # paso: golpe grave corto
    guardar("paso", tono(lambda t: 90 - 40 * t / 0.12, 0.12, "seno", 0.9, 0.002, 0.1))

    # servo: motor que sube de tono (brazos, agacharse, giro)
    guardar("servo", tono(lambda t: 300 + 500 * t / 0.4, 0.4, "diente", 0.35, 0.02, 0.1, vibrato=0.02))

    # saludo: dos bips alegres
    guardar("saludo", concatenar(tono(880, 0.08, "cuadrado", 0.35, 0.002, 0.03),
                                 silencio(0.04),
                                 tono(1320, 0.12, "cuadrado", 0.35, 0.002, 0.08)))

    # alerta: sirena de dos tonos
    guardar("alerta", concatenar(*[concatenar(tono(700, 0.2, "cuadrado", 0.3, 0.005, 0.02),
                                              tono(500, 0.2, "cuadrado", 0.3, 0.005, 0.02))
                                   for _ in range(2)]))

    # heroe: arpegio triunfal
    notas = [523, 659, 784, 1047]
    guardar("heroe", concatenar(*[tono(f, 0.14, "seno", 0.45, 0.005, 0.12) for f in notas]))

    # sonrisa: chirrido feliz que sube
    guardar("sonrisa", tono(lambda t: 600 + 350 * t / 0.22, 0.22, "seno", 0.5, 0.01, 0.1))

    # guiño: un blip corto y pícaro
    guardar("guino", tono(lambda t: 1200 - 500 * t / 0.1, 0.1, "seno", 0.5, 0.005, 0.06))

    # tristeza: bajada lenta
    guardar("tristeza", tono(lambda t: 520 - 280 * t / 0.7, 0.7, "seno", 0.5, 0.05, 0.3, vibrato=0.01))

    # miedo: temblor rápido
    guardar("miedo", [v * (0.6 + 0.4 * math.sin(2 * math.pi * 14 * i / RATE))
                      for i, v in enumerate(tono(330, 0.6, "diente", 0.4, 0.02, 0.2))])

    # enojo: zumbido grave y áspero
    guardar("enojo", tono(110, 0.5, "cuadrado", 0.4, 0.01, 0.15))

    # admiración: campanitas ascendentes
    guardar("admiracion", concatenar(tono(660, 0.15, "seno", 0.4, 0.005, 0.12),
                                     tono(880, 0.15, "seno", 0.4, 0.005, 0.12),
                                     tono(1320, 0.4, "seno", 0.4, 0.005, 0.35)))

    # choque: golpe seco con un barrido hacia abajo
    guardar("choque", concatenar(tono(lambda t: 500 - 380 * t / 0.25, 0.25, "cuadrado", 0.45, 0.002, 0.2),
                                 silencio(0.05)))

    # duda: tono que vibra de lado a lado
    guardar("duda", tono(lambda t: 420 + 80 * math.sin(2 * math.pi * 5 * t), 0.5, "seno", 0.45, 0.02, 0.2))


# ============================================================
# AMBIENTES (uno por escenario, en bucle)
# ============================================================

def ambiente_taller():
    dur = 6.0
    n = int(dur * RATE)
    zumbido = tono(60, dur, "seno", 0.18)
    golpes = [0.0] * n
    rnd = random.Random(3)
    for inicio in (0.4, 1.9, 3.1, 4.6, 5.4):              # martillazos
        for i in range(int(0.25 * RATE)):
            k = int(inicio * RATE) + i
            if k < n:
                golpes[k] += rnd.uniform(-1, 1) * math.exp(-i / (0.02 * RATE)) * 0.6
    engranaje = tono(lambda t: 8 + 2 * math.sin(t), dur, "cuadrado", 0.05)
    return loop(mezclar(zumbido, golpes, engranaje), 0.5)


def ambiente_neon():
    dur = 6.0
    acordes = concatenar(tono(220, 2, "seno", 0.18), tono(261, 2, "seno", 0.18), tono(329, 2, "seno", 0.18))
    arpegio = []
    for f in [440, 523, 659, 523] * 12:  # 12 compases de 0.5 s = 6 s
        arpegio.extend(tono(f, 0.0625 * 2, "cuadrado", 0.06, 0.003, 0.03))
    pad = concatenar(tono(110, dur, "seno", 0.12))
    return loop(mezclar(acordes[: int(dur * RATE)], arpegio[: int(dur * RATE)], pad[: int(dur * RATE)]), 0.5)


def ambiente_desierto():
    dur = 6.0
    n = int(dur * RATE)
    viento = ruido_suave(n, 0.01, seed=7)
    viento = [v * (0.5 + 0.5 * math.sin(2 * math.pi * i / n)) * 0.5 for i, v in enumerate(viento)]
    flauta = tono(lambda t: 392 + 6 * math.sin(2 * math.pi * 4 * t), dur, "seno", 0.12, 0.5, 0.5)
    return loop(mezclar(viento, flauta), 0.5)


def ambiente_volcan():
    dur = 6.0
    n = int(dur * RATE)
    rumble = ruido_suave(n, 0.004, seed=11)
    grave = tono(45, dur, "seno", 0.25)
    rnd = random.Random(5)
    chasquidos = [0.0] * n
    for _ in range(14):
        k = rnd.randrange(n)
        for i in range(int(0.03 * RATE)):
            if k + i < n:
                chasquidos[k + i] += rnd.uniform(-1, 1) * math.exp(-i / (0.005 * RATE)) * 0.5
    return loop(mezclar(rumble, grave, chasquidos), 0.5)


def ambiente_glaciar():
    dur = 6.0
    n = int(dur * RATE)
    viento = ruido_suave(n, 0.02, seed=21)
    campanas = [0.0] * n
    for inicio, f in ((0.3, 1046), (2.1, 1318), (3.6, 1568), (5.0, 1046)):
        pista = tono(f, 1.2, "seno", 0.12, 0.003, 1.0)
        for i, v in enumerate(pista):
            if int(inicio * RATE) + i < n:
                campanas[int(inicio * RATE) + i] += v
    return loop(mezclar([v * 0.4 for v in viento], campanas), 0.5)


def ambiente_cristal():
    dur = 6.0
    n = int(dur * RATE)
    pentatonica = [523, 587, 659, 784, 880]
    rnd = random.Random(9)
    pistas = [0.0] * n
    for k in range(12):
        f = rnd.choice(pentatonica)
        pluck = tono(f, 0.9, "seno", 0.25, 0.002, 0.8)
        inicio = int(k * 0.5 * RATE)
        for i, v in enumerate(pluck):
            if inicio + i < n:
                pistas[inicio + i] += v
    pad = tono(262, dur, "seno", 0.08)
    return loop(mezclar(pistas, pad), 0.5)


def ambiente_luna():
    dur = 6.0
    n = int(dur * RATE)
    drone = mezclar(tono(55, dur, "seno", 0.2), tono(82.5, dur, "seno", 0.12))
    drone = [v * (0.7 + 0.3 * math.sin(2 * math.pi * i / n)) for i, v in enumerate(drone)]
    rnd = random.Random(4)
    estatica = [0.0] * n
    for inicio in (1.0, 3.5):
        for i in range(int(0.4 * RATE)):
            if int(inicio * RATE) + i < n:
                estatica[int(inicio * RATE) + i] = rnd.uniform(-1, 1) * 0.25
    return loop(mezclar(drone, estatica), 0.5)


if __name__ == "__main__":
    os.makedirs(DESTINO, exist_ok=True)
    efectos()
    guardar("amb_taller", ambiente_taller(), 0.5)
    guardar("amb_neon", ambiente_neon(), 0.5)
    guardar("amb_desierto", ambiente_desierto(), 0.5)
    guardar("amb_volcan", ambiente_volcan(), 0.5)
    guardar("amb_glaciar", ambiente_glaciar(), 0.5)
    guardar("amb_cristal", ambiente_cristal(), 0.5)
    guardar("amb_luna", ambiente_luna(), 0.5)
