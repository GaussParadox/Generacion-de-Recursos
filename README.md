# AssetsIA_ParejaN

Proyecto de Godot 4.5 del taller **Producción de assets para videojuegos con inteligencia artificial**
(Diseño Multimedia y Videojuegos, FESC, Ingeniería de Software IX).

- **Integrantes:** Wilson Alejandro Saavedra Arenales y Oscar Andres Arciniegas Bustos
- **Repositorio público:** (https://github.com/GaussParadox/Generacion-de-Recursos)
- **Motor:** Godot 4.5

## Cómo abrir y jugar

1. Instale [Git LFS](https://github.com/git-lfs/git-lfs) y ejecute `git lfs install` una sola vez.
2. Clone el repositorio: `git clone <enlace>`.
3. Abra Godot 4.5 → Import → seleccione `project.godot`. La primera vez Godot importa todos los assets.
4. Ejecute con F5 (escena principal: `escenas/main.tscn`).

Controles: **flechas** para moverse, **espacio / Enter / ↑** para saltar, **C** para ver el cofre 3D
(**Esc** o **C** para volver). Acérquese al guardián (extremo derecho del nivel) para hablar.
Caer a un hueco reinicia al personaje con sonido y chispas de daño.

## Qué contiene cada nivel requerido del documento

| Nivel | Contenido en el proyecto |
|---|---|
| 1 Guía de estilo | `docs/guia_estilo.md`, `docs/paleta.png` (16 colores), 5 imágenes en `docs/referencias/` |
| 2 Personaje 2D | `assets/sprites/personaje_sheet.png` (8 cuadros de 32x32), `escenas/jugador.tscn` con SpriteFrames `quieto` y `caminar` |
| 3 TileMapLayer | `assets/tiles/tileset_bosque.png`, `assets/tiles/tileset.tres` (física, una baldosa de un solo sentido), `escenas/nivel.tscn` con dos TileMapLayer |
| 4 Modelo 3D PBR | `assets/modelos/cofre.glb`, `assets/texturas/madera_*.png`, `madera.tres`, `escenas/cofre_3d.tscn` |
| 5 Partículas | `assets/vfx/chispa.png`, `escenas/chispas.tscn` (GPUParticles2D, One Shot) |
| 6 Audio | `assets/audio/musica.ogg` (16 s, bucle), `salto.wav`, `recoger.wav`, `dano.wav`, buses `Musica` y `SFX` |
| 7 Interfaz y diálogos | `escenas/interfaz.tscn`, `assets/sprites/ui_*.png`, `escenas/dialogos/guardian.dialogue` |
| 8 Flujo profesional | estructura de carpetas, Git LFS, `.gitignore`, `docs/registro_assets.md` |

## Estructura

```
assets/
  sprites/    personaje, guardián e interfaz (niveles 2 y 7)
  tiles/      atlas y TileSet (nivel 3)
  modelos/    cofre.glb (nivel 4)
  texturas/   albedo, normal, roughness y madera.tres (nivel 4)
  audio/      musica.ogg y efectos .wav (nivel 6)
  vfx/        textura de partícula (nivel 5)
escenas/      main, jugador, nivel, moneda, chispas, interfaz, cofre_3d, dialogos/
scripts/      GDScript de cada escena
addons/       (vacío) Dialogue Manager / Dialogic 2 si lo instalan
docs/
  guia_estilo.md        nivel 1
  registro_assets.md    nivel 8 (tabla 13)
  comandos.md           comandos de apoyo (rembg, Piper, Git LFS)
  checklist_niveles.md  lista de verificación por nivel
  herramientas/         generar_assets.py (origen de todos los assets)
  referencias/          imágenes de referencia de estilo
  capturas/             capturas de cada nivel (ver LEEME.md)
```

## Origen de los assets

Todos los assets incluidos se generaron con código (`docs/herramientas/generar_assets.py`: Pillow, NumPy y
ffmpeg), sin modelos de terceros ni material con licencia, y están registrados en `docs/registro_assets.md`.
Son una base funcional: el taller pide retocarlos o reemplazarlos con sus propias herramientas
(Pixelorama, Krita, Blender, ComfyUI, Meshy, etc.) y anotar el cambio en el registro.

Para regenerarlos: `python3 docs/herramientas/generar_assets.py .` desde la raíz del proyecto
(requiere Python 3.10+, Pillow, NumPy y ffmpeg).

## Qué falta por hacer a la pareja

- Abrir el proyecto en Godot 4.5, comprobar que corre y tomar las capturas reales de cada nivel en `docs/capturas/`.
- Retocar o reemplazar los assets con su propia temática y actualizar `docs/registro_assets.md`.
- Opcional: instalar Dialogue Manager desde AssetLib (el archivo `.dialogue` ya usa su sintaxis).
- Escribir los nombres de los integrantes y el enlace del repositorio arriba.

## Configuración incluida

- Filtro de textura por defecto **Nearest** (pixel art).
- Buses de audio **Musica** y **SFX** (`default_bus_layout.tres`).
- Git LFS para `*.png`, `*.glb`, `*.wav`, `*.ogg` (`.gitattributes`) y `.gitignore` que excluye `.godot/`.
