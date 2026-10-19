# Registro de assets (Nivel 8, Tabla 13)

Una fila por asset. Cualquier asset de licencia no comercial (Suno, ElevenLabs, Krea y Tripo en plan gratis;
MusicGen; FLUX.1 [dev]; BRIA RMBG-2.0; Coqui XTTS-v2) debe marcarse con **[PROTOTIPO]** y reemplazarse antes de publicar.

**Estado actual: ningún asset es de prototipo.** Todo lo de la tabla se generó con un script propio
(`docs/herramientas/generar_assets.py`: Pillow, NumPy y ffmpeg), sin modelos de IA de terceros ni material con licencia.
Se creó con ayuda de un asistente de IA (Claude) que escribió el código; el resultado es obra del equipo, sin restricciones
de uso ni atribución obligatoria.

| Asset | Herramienta y modelo | Prompt o fuente | Licencia | Modificación |
|---|---|---|---|---|
| sprites/personaje_sheet.png | Script Python (Pillow) | Explorador del bosque dibujado por código: 8 cuadros de 32x32 (4 quieto + 4 caminar) | Obra propia, uso comercial libre | Contorno automático; paleta de 16 colores; pendiente retocar en Pixelorama |
| sprites/guardian.png | Script Python (Pillow) | Guardián encapuchado con bastón, 32x32 | Obra propia, uso comercial libre | Paleta de 16 colores |
| sprites/ui_marco.png | Script Python (Pillow) | Marco 9-patch de 48x48 para el diálogo | Obra propia, uso comercial libre | Paleta de 16 colores |
| sprites/ui_moneda.png | Script Python (Pillow) | Moneda 16x16 | Obra propia, uso comercial libre | Paleta de 16 colores |
| sprites/ui_corazon.png | Script Python (Pillow) | Corazón 16x16 (disponible para vidas) | Obra propia, uso comercial libre | Paleta de 16 colores |
| tiles/tileset_bosque.png | Script Python (Pillow) | Atlas 4x2 de 32x32: pasto, tierra, ladrillo, ladrillo con musgo, plataforma, arbusto, hongo, enredadera | Obra propia, uso comercial libre | Paleta de 16 colores; física definida en `tiles/tileset.tres` |
| vfx/chispa.png | Script Python (Pillow) | Chispa 8x8 para GPUParticles2D | Obra propia, uso comercial libre | Paleta de 16 colores |
| texturas/madera_albedo.png | Script Python (NumPy) | Tablas de madera procedurales, 256x256 | Obra propia, uso comercial libre | — |
| texturas/madera_normal.png | Script Python (NumPy) | Mapa normal estilo OpenGL derivado del mapa de altura de la madera | Obra propia, uso comercial libre | — |
| texturas/madera_roughness.png | Script Python (NumPy) | Rugosidad procedural de la madera | Obra propia, uso comercial libre | — |
| modelos/cofre.glb | Script Python (glTF escrito a mano) | Cofre low poly de 1 x 0.7 x 0.6 m, 132 vértices, origen en la base | Obra propia, uso comercial libre | Escala y origen definidos en el script |
| audio/musica.ogg | Script Python (NumPy) + ffmpeg (libvorbis) | Chiptune en Do mayor, 120 bpm, 8 compases en bucle | Obra propia, uso comercial libre | Cargada con Loop activado desde `scripts/main.gd` |
| audio/salto.wav | Script Python (NumPy) | Barrido ascendente de onda cuadrada, 0,22 s | Obra propia, uso comercial libre | — |
| audio/recoger.wav | Script Python (NumPy) | Dos tonos agudos de onda cuadrada, 0,29 s | Obra propia, uso comercial libre | — |
| audio/dano.wav | Script Python (NumPy) | Ruido y barrido descendente de onda de sierra, 0,38 s | Obra propia, uso comercial libre | — |
| escenas/dialogos/guardian.dialogue | Escrito a mano (asistente de IA) | Diálogo corto en español con dos opciones de respuesta | Obra propia, uso comercial libre | Sintaxis de Dialogue Manager |
| docs/paleta.png | Script Python (Pillow) | Paleta de 16 colores | Obra propia, uso comercial libre | — |

## Atribuciones requeridas

Ninguna por ahora. Si se agrega un modelo de Meshy (CC BY 4.0) o una voz de Piper entrenada con datos CC BY, citar aquí al autor o al servicio.
