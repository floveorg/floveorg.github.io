# Pandas · un GIF animado por emoción

Un GIF por emoción, **igual que el del neutral** (`../animated/`): fotogramas
SVG planos rasterizados con cairosvg y montados en un GIF en bucle. **Cada
emoción en su propia carpeta** (`<emoción>/`) con sus `frame-00..11.svg` y su
`panda-<emoción>.gif`.

A diferencia del neutral (que tiene su `gen_frames.py` a mano), aquí los 10 se
generan con un único script que **hornea la animación expresiva** (la misma de
`../animated/expressive/`, en CSS) en fotogramas: toma cada pose estática de
`../expressive/panda-<emoción>.svg` y le inyecta los transforms por fotograma
(cabeza, brazos, pies, ojos, boca, cuerpo, iconos, color).

| emoción | qué hace el GIF |
|---|---|
| celebrando | salta y agita los brazos, estrellas que parpadean |
| feliz | rebota, bracitos meneando, parpadeo, destellos |
| enamorado | suspira, ojos-corazón latiendo, corazones que suben |
| guiño | ladea, saluda, parpadeo + destello |
| sorprendido | respingo, brazos arriba, boca-O, ❗ que aparece |
| pensativo | ladea y mira, burbujas de pensamiento |
| preocupado | inquieto, gota de sudor que resbala |
| triste | suspiro, lágrima que cae |
| enfadado | tiembla, mejillas rojas, vena que late |
| dormido | respira lento, zZ flotando |

## Regenerar
```bash
# necesita cairosvg + pillow (reutiliza el venv del neutral):
../animated/.venv/bin/python gen_all.py
```
Ajusta fotogramas (`N`), tamaño (`SIZE`) o los tiempos/movimiento por emoción
en `gen_all.py` (función `motion`).
