# state.py
# Estado compartido entre los módulos (audio, entrada, etc.)

# Sonidos cargados: nombre -> pygame.mixer.Sound (o None si falló)
sounds = {}

# Último sonido reproducido
last_sound = None

# Volumen general (0.0 a 1.0) y estado de silencio
volume = 1.0
muted = False
