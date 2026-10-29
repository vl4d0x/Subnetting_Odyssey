# audio.py
# Sonido del proyecto: efectos de expresiones y movimientos, y un ambiente
# en bucle por escenario. Todo se controla con un solo interruptor general (M).

import os
import pygame

from actions import state


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SOUNDS_DIR = os.path.join(PROJECT_ROOT, "utils", "sonidos")


# ============================================================
# ARCHIVOS DE SONIDO (creados con utils/generar_sonidos.py)
# ============================================================

SOUND_FILES = {
    # expresiones
    "sonrisa": "sonrisa.wav",
    "guino": "guino.wav",
    "tristeza": "tristeza.wav",
    "miedo": "miedo.wav",
    "enojo": "enojo.wav",
    "admiracion": "admiracion.wav",
    "duda": "duda.wav",

    # movimientos
    "salto": "salto.wav",
    "paso": "paso.wav",
    "servo": "servo.wav",
    "saludo": "saludo.wav",
    "alerta": "alerta.wav",
    "heroe": "heroe.wav",
    "choque": "choque.wav",

    # ambientes de cada escenario (en bucle)
    "amb_taller": "amb_taller.wav",
    "amb_neon": "amb_neon.wav",
    "amb_desierto": "amb_desierto.wav",
    "amb_volcan": "amb_volcan.wav",
    "amb_glaciar": "amb_glaciar.wav",
    "amb_cristal": "amb_cristal.wav",
    "amb_luna": "amb_luna.wav",
}

# El canal 0 queda reservado para el ambiente, así un efecto no lo corta.
CANAL_AMBIENTE = 0


# ============================================================
# INICIALIZACIÓN
# ============================================================

def init_audio():
    """Inicializa el mixer de pygame y carga todos los sonidos."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as e:
        print("Error inicializando el audio:", e)
        return

    pygame.mixer.set_num_channels(8)
    pygame.mixer.set_reserved(1)

    for name, filename in SOUND_FILES.items():
        path = os.path.join(SOUNDS_DIR, filename)
        try:
            state.sounds[name] = pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Error cargando sonido '{name}': {e}")
            state.sounds[name] = None

    _apply_volume()


# ============================================================
# EFECTOS
# ============================================================

def play_sound(name):
    """Reproduce un efecto una vez: play_sound("salto")."""
    sound = state.sounds.get(name)
    if sound is None:
        return
    try:
        sound.play()
        state.last_sound = name
    except pygame.error as e:
        print(f"Error reproduciendo sonido '{name}': {e}")


def stop_sound(name):
    sound = state.sounds.get(name)
    if sound is not None:
        sound.stop()


def stop_all_sounds():
    """Detiene todos los sonidos (tecla 0)."""
    try:
        pygame.mixer.stop()
        state.last_sound = None
    except pygame.error as e:
        print("Error deteniendo los sonidos:", e)


# ============================================================
# AMBIENTE POR ESCENARIO
# ============================================================

def play_ambient(name):
    """Cambia el ambiente en bucle sin cortar los efectos."""
    sound = state.sounds.get(name)
    if sound is None:
        return
    try:
        pygame.mixer.Channel(CANAL_AMBIENTE).play(sound, loops=-1)
        state.last_sound = name
    except pygame.error as e:
        print(f"Error reproduciendo ambiente '{name}': {e}")


# ============================================================
# VOLUMEN GENERAL Y SILENCIO
# ============================================================

def _apply_volume():
    """Aplica a todos los sonidos el volumen actual (0 si está muteado)."""
    effective = 0.0 if state.muted else state.volume
    for sound in state.sounds.values():
        if sound is not None:
            sound.set_volume(effective)


def toggle_mute():
    """Sonido general ON / OFF (tecla M). Los sonidos siguen corriendo en silencio."""
    state.muted = not state.muted
    _apply_volume()


def shutdown_audio():
    try:
        pygame.mixer.stop()
        pygame.mixer.quit()
    except pygame.error as e:
        print("Error cerrando el audio:", e)
    state.sounds.clear()
    state.last_sound = None
