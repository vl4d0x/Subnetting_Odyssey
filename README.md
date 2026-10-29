# Mecha-7 · Mecha de Graficación

Personaje 3D interactivo hecho con Python, PyOpenGL (GLUT) y pygame.
Proyecto 2 de la materia Graficación · Instituto Tecnológico de Toluca.

## Requisitos

- Python 3.10 o superior
- Paquetes: `pip install PyOpenGL pygame`
- GLUT del sistema (en Linux/Debian: `sudo apt install freeglut3`)

## Ejecutar

```bash
python main.py
```

Los sonidos ya vienen generados en `utils/sonidos/`. Si los borras, se pueden
volver a crear con `python utils/generar_sonidos.py`.

## Controles

Expresiones: `1`–`7` · Movimientos: `Espacio` saltar, `V` caminar, `Z`/`X` brazos,
`C` agacharse, `T` inclinarse, `K` pose de héroe, `B` girar, `G` saludar, `L` alerta ·
Escenarios: `F1`–`F7` o `N` · Cámara: flechas, `W A S D`, `Q E`, rueda, arrastrar con
el mouse, `R` cámara normal · General: `M` sonido ON/OFF, `0` detener sonidos,
`H` instrucciones, `I` acerca de, clic central menú, `ESC` salir.

## Estructura

```
main.py              ventana, ciclo de dibujo y configuración de luz
characters/          Mecha-7 (cuerpo, brazos, piernas, cabeza, visor)
actions/             expresiones, movimientos y estado compartido
scenes/              los 7 escenarios
resources/           cámara, audio, teclas, interfaz (HUD) y datos "Acerca de"
utils/               generador de sonidos y archivos WAV
```
