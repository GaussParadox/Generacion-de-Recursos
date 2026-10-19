# Comandos de apoyo

## Quitar fondo con rembg (nivel 2)

Use siempre `-m isnet-general-use` (sin `-m` descarga el modelo BRIA, no comercial).

```bash
pip install "rembg[cpu,cli]"
rembg i -m isnet-general-use entrada.png salida.png
rembg p -m isnet-general-use carpeta_entrada carpeta_salida
```

## Voz en español con Piper (nivel 6, opcional)

```bash
pip install piper-tts
python -m piper.download_voices es_MX-claude-high
echo "Bienvenido, viajero." | python -m piper -m es_MX-claude-high -f voz_intro.wav
```

## Diálogo con modelo local (nivel 7)

```bash
ollama run qwen2.5-coder:7b
```

Prompt: «Escribe un diálogo corto en español entre un explorador y un guardián del bosque,
con dos opciones de respuesta, en formato de Dialogue Manager para Godot 4». Revise y corrija el resultado.

## Git y Git LFS (nivel 8)

```bash
git init
git lfs install
git lfs track "*.png" "*.glb" "*.wav" "*.ogg"
git add .gitattributes .
git commit -m "Proyecto base"
git remote add origin <enlace>
git push -u origin main
```

## Volumen de un bus desde script

```gdscript
AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Musica"), -6.0)
```
