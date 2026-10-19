# Guía de estilo (Nivel 1)

## Temática y vista

- Temática: explorador de un bosque fantástico que recoge monedas y habla con un guardián.
- Vista: plataformas 2D de lado (side view) en pixel art; objeto 3D low poly (cofre de madera) como vitrina del nivel 4.

## Visual

- Resolución de los sprites: **32x32 px** por cuadro.
- Tamaño de baldosa: **32x32 px** (atlas de 4x2 en `assets/tiles/tileset_bosque.png`).
- Contornos: limpios, 1 px, color `#171a26`.
- Paleta de 16 colores: `docs/paleta.png` (y `docs/paleta_16x1.png` para importarla en Pixelorama).
- Escalado: solo por factor entero (2x, 3x, 4x) con filtro Nearest; sin escalado con IA para pixel art.
- Cámara 2D con zoom 3x sobre un viewport de 1152x648.

| # | Color | Uso |
|---|---|---|
| 0 | `#171a26` | contornos, sombras profundas |
| 1 | `#2f3a4a` | pizarra: fondo de interfaz, mortero |
| 2 | `#4b5d67` | piedra |
| 3 | `#8aa0a6` | piedra clara, brillos |
| 4 | `#e9e6d8` | hueso: texto, brillos |
| 5 | `#1f4d2e` | verde oscuro |
| 6 | `#2f7a3c` | verde medio |
| 7 | `#6fb04a` | verde claro |
| 8 | `#b9d96a` | lima, brillos de pasto |
| 9 | `#4a2c1d` | tierra oscura, botas |
| 10 | `#7a4a2a` | tierra |
| 11 | `#b57a43` | madera, piel |
| 12 | `#e0b15a` | dorado: monedas, chispas |
| 13 | `#a8322f` | rojo |
| 14 | `#e8704a` | naranja |
| 15 | `#5ab5d6` | cielo |

## Sonoro

- Música: chiptune aventurero en Do mayor, 120 bpm, instrumental, 8 compases (16 s) en bucle; melodía en onda cuadrada, bajo triangular y percusión de ruido.
- Efectos: estilo retro de 8 bits, cortos (salto, recoger, daño), exportados como WAV mono.
- Mezcla: música por el bus `Musica` (-6 dB) y efectos por el bus `SFX`.

## Textos

- Tono: amistoso, misterioso y breve.
- Idioma: español. Interfaz y diálogos en frases cortas.
- Personajes: el explorador (jugador) y el guardián del bosque.

## Prompts base (bloque de estilo común)

```
pixel art, 32x32 sprite, side view, limited 16-color palette, clean outlines,
fantasy forest explorer, flat background, game asset
```

Negativo (SD): `blurry, gradient, photo, text, watermark`

## Imágenes de referencia

Cinco imágenes con la misma paleta y estilo en `docs/referencias/`: personaje, guardián, baldosas, objetos e interfaz.
