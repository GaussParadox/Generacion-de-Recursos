# Checklist por nivel

Leyenda: `[x]` ya incluido en el proyecto · `[ ]` lo debe hacer la pareja.

## Nivel 1. Guía de estilo (0,5)
- [x] `docs/paleta.png` con 16 colores
- [x] 5 imágenes de referencia con el mismo estilo (`docs/referencias/`)
- [x] `docs/guia_estilo.md` completo

## Nivel 2. Personaje 2D animado (0,7)
- [x] Spritesheet en una fila: `assets/sprites/personaje_sheet.png`
- [x] Default Texture Filter = Nearest (en `project.godot`)
- [x] CharacterBody2D + AnimatedSprite2D con animaciones `quieto` y `caminar`

## Nivel 3. TileMapLayer (0,6)
- [x] Atlas de baldosas propio (`assets/tiles/tileset_bosque.png`)
- [x] TileMapLayer (no TileMap) con Physics Layer en el TileSet (`assets/tiles/tileset.tres`)
- [x] Nivel recorrible (`escenas/nivel.tscn`, mapa en `scripts/nivel.gd`)

## Nivel 4. Modelo 3D con PBR (0,7)
- [x] `.glb` limpio en `assets/modelos/cofre.glb`
- [x] Mapas Albedo, Normal (OpenGL) y Roughness en `assets/texturas/`
- [x] StandardMaterial3D (`madera.tres`), DirectionalLight3D, Camera3D, WorldEnvironment (`escenas/cofre_3d.tscn`)

## Nivel 5. GPUParticles (0,4)
- [x] Textura de partícula en `assets/vfx/chispa.png`
- [x] GPUParticles2D con ParticleProcessMaterial (One Shot, Explosiveness = 1)
- [x] Se activa con `restart()` al recoger monedas y al caer

## Nivel 6. Audio (0,6)
- [x] `assets/audio/musica.ogg` en bucle
- [x] 3 efectos WAV (salto, recoger, daño)
- [x] Buses Musica y SFX (`default_bus_layout.tres`)

## Nivel 7. Interfaz y diálogos (0,5)
- [x] Diálogo con dos opciones (`escenas/dialogos/guardian.dialogue`)
- [x] Se abre al acercarse al guardián (Area2D, body_entered)
- [x] Interfaz coherente con la guía de estilo (marco 9-patch, moneda, HUD)

## Nivel 8. Flujo profesional (0,4 + 0,6)
- [x] Estructura de carpetas, Git LFS y `.gitignore`
- [x] `docs/registro_assets.md` con todos los assets y ninguno de prototipo
- [ ] Capturas reales de cada nivel en `docs/capturas/`
- [ ] Subir al repositorio público y poner el enlace en el README y en la portada del documento
- [ ] Actualizar el registro si cambian o agregan assets
