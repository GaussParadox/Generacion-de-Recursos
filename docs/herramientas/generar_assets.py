#!/usr/bin/env python3
"""Generador procedural de los assets del taller (Godot 4.5).

Uso: python3 generar_assets.py <ruta_del_proyecto>

Todo lo que produce este script es obra propia del equipo (sin modelos de IA de
terceros ni material con licencia): pixel art dibujado por código con Pillow,
texturas PBR con NumPy, modelo 3D escrito directamente como glTF binario (.glb),
audio sintetizado con NumPy y convertido a OGG con ffmpeg.
"""
import json
import math
import os
import random
import struct
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."


def P(*partes):
    ruta = os.path.join(ROOT, *partes)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    return ruta


# ---------------------------------------------------------------- paleta (nivel 1)
PALETA_HEX = [
    "#171a26", "#2f3a4a", "#4b5d67", "#8aa0a6",  # 0-3  noche, pizarra, piedra, piedra clara
    "#e9e6d8", "#1f4d2e", "#2f7a3c", "#6fb04a",  # 4-7  hueso, verdes
    "#b9d96a", "#4a2c1d", "#7a4a2a", "#b57a43",  # 8-11 lima, tierras, madera
    "#e0b15a", "#a8322f", "#e8704a", "#5ab5d6",  # 12-15 dorado, rojo, naranja, cielo
]
PAL = [tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for h in PALETA_HEX]
T = (0, 0, 0, 0)


def new(w, h):
    return Image.new("RGBA", (w, h), T)


def col(c):
    return PAL[c] if isinstance(c, int) else c


def px(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), col(c))


def rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, c)


def outline(img, c=0):
    src = img.copy()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if src.getpixel((x, y))[3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and src.getpixel((nx, ny))[3] > 0:
                        img.putpixel((x, y), PAL[c])
                        break
    return img


def escalar(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def guardar(img, *ruta):
    img.save(P(*ruta))


# paleta
sw = new(16 * 32, 32)
for i in range(16):
    rect(sw, i * 32, 0, i * 32 + 31, 31, i)
guardar(sw, "docs", "paleta.png")
sw1 = new(16, 1)
for i in range(16):
    px(sw1, i, 0, i)
guardar(sw1, "docs", "paleta_16x1.png")


# ---------------------------------------------------------------- personaje (nivel 2)
def personaje(frame):
    img = new(32, 32)
    caminar = frame >= 4
    k = frame % 4
    if not caminar:
        bob = [0, 0, -1, -1][k]
        pata_a = (12, 14, 23, 30)
        pata_b = (17, 19, 23, 30)
        brazo_dx = 0
    else:
        bob = [0, -1, 0, -1][k]
        pata_a, pata_b = [
            ((10, 12, 23, 30), (18, 20, 23, 30)),
            ((13, 15, 23, 29), (16, 18, 23, 30)),
            ((18, 20, 23, 30), (10, 12, 23, 30)),
            ((16, 18, 23, 30), (13, 15, 23, 29)),
        ][k]
        brazo_dx = [-2, 0, 2, 0][k]
    # piernas (A atrás, más oscura; B delante)
    for (x0, x1, y0, y1), c in ((pata_a, 1), (pata_b, 2)):
        rect(img, x0, y0, x1, y1, c)
        rect(img, x0, y1 - 1, x1 + 1, y1, 9)  # botas
    # mochila
    rect(img, 8, 17 + bob, 10, 22 + bob, 10)
    rect(img, 8, 21 + bob, 10, 22 + bob, 9)
    # torso
    rect(img, 11, 16 + bob, 20, 23, 6)
    rect(img, 11, 16 + bob, 11, 23, 5)
    rect(img, 11, 21, 20, 21, 9)
    px(img, 16, 21, 12)
    # brazo
    rect(img, 15 + brazo_dx, 17 + bob, 17 + brazo_dx, 21 + bob, 7)
    rect(img, 15 + brazo_dx, 22 + bob, 17 + brazo_dx, 22 + bob, 11)
    # cabeza
    rect(img, 12, 9 + bob, 19, 15 + bob, 11)
    rect(img, 12, 9 + bob, 12, 15 + bob, 10)
    px(img, 18, 12 + bob, 0)
    px(img, 20, 12 + bob, 11)
    rect(img, 12, 9 + bob, 14, 10 + bob, 9)  # flequillo
    # sombrero con pluma
    rect(img, 12, 4 + bob, 19, 7 + bob, 6)
    rect(img, 10, 8 + bob, 21, 8 + bob, 5)
    rect(img, 12, 7 + bob, 19, 7 + bob, 5)
    rect(img, 20, 4 + bob, 22, 5 + bob, 14)
    px(img, 22, 3 + bob, 12)
    return outline(img, 0)


def guardian():
    img = new(32, 32)
    rect(img, 11, 5, 20, 12, 5)  # capucha
    rect(img, 15, 8, 19, 11, 0)
    px(img, 16, 9, 12)
    px(img, 18, 9, 12)
    for y in range(13, 31):
        half = 5 + (y - 13) // 3
        rect(img, 16 - half, y, 16 + half, y, 6)
        px(img, 16 - half, y, 5)
        px(img, 16 + half, y, 5)
    rect(img, 11, 20, 21, 20, 9)
    rect(img, 24, 6, 24, 30, 11)  # bastón
    rect(img, 23, 3, 25, 5, 15)
    px(img, 23, 3, 4)
    rect(img, 22, 18, 24, 19, 11)
    return outline(img, 0)


hoja = new(32 * 8, 32)
for f in range(8):
    hoja.paste(personaje(f), (32 * f, 0))
guardar(hoja, "assets", "sprites", "personaje_sheet.png")
guardar(guardian(), "assets", "sprites", "guardian.png")


# ---------------------------------------------------------------- baldosas (nivel 3)
def t_pasto():
    img = new(32, 32)
    rng = random.Random(1)
    rect(img, 0, 8, 31, 31, 10)
    for _ in range(46):
        px(img, rng.randrange(32), rng.randrange(10, 32), rng.choice([9, 11, 9]))
    for _ in range(4):
        x, y = rng.randrange(1, 30), rng.randrange(14, 30)
        px(img, x, y, 2)
        px(img, x + 1, y, 3)
    rect(img, 0, 0, 31, 6, 6)
    rect(img, 0, 0, 31, 1, 7)
    for x in range(32):
        if rng.random() < 0.3:
            px(img, x, 0, 8)
        extra = rng.randint(0, 3)
        rect(img, x, 7, x, 7 + extra, 6)
        px(img, x, 8 + extra, 5)
    return img


def t_tierra():
    img = new(32, 32)
    rng = random.Random(2)
    rect(img, 0, 0, 31, 31, 10)
    for _ in range(60):
        px(img, rng.randrange(32), rng.randrange(32), rng.choice([9, 11, 9]))
    for _ in range(5):
        x, y = rng.randrange(1, 30), rng.randrange(1, 30)
        px(img, x, y, 2)
        px(img, x + 1, y, 3)
        px(img, x, y + 1, 1)
    return img


def t_ladrillo(musgo=False):
    img = new(32, 32)
    rng = random.Random(3 if not musgo else 4)
    rect(img, 0, 0, 31, 31, 2)
    for r in range(4):
        y0 = r * 8
        rect(img, 0, y0 + 7, 31, y0 + 7, 1)
        for i in range(2):
            xj = ((r % 2) * 8 + 16 * i) % 32
            rect(img, xj, y0, xj, y0 + 6, 1)
        for x in range(32):
            if img.getpixel((x, y0))[:3] == PAL[2][:3]:
                px(img, x, y0, 3)
    for _ in range(18):
        px(img, rng.randrange(32), rng.randrange(32), rng.choice([1, 3]))
    if musgo:
        for r in range(4):
            for x in range(32):
                if rng.random() < 0.28:
                    h = rng.randint(1, 3)
                    for d in range(h):
                        px(img, x, r * 8 + d, 6 if d else 7)
    return img


def t_plataforma():
    img = new(32, 32)
    rect(img, 0, 0, 31, 7, 11)
    rect(img, 0, 0, 31, 0, 12)
    rect(img, 0, 7, 31, 7, 9)
    rect(img, 15, 1, 15, 6, 9)
    rect(img, 31, 1, 31, 6, 9)
    px(img, 3, 3, 3)
    px(img, 12, 3, 3)
    px(img, 19, 3, 3)
    px(img, 28, 3, 3)
    return img


def t_arbusto():
    img = new(32, 32)
    d = ImageDraw.Draw(img)
    d.ellipse([4, 14, 28, 38], fill=PAL[5])
    d.ellipse([5, 14, 27, 34], fill=PAL[6])
    d.ellipse([8, 15, 20, 24], fill=PAL[7])
    for (x, y) in ((11, 20), (21, 24), (16, 27)):
        px(img, x, y, 13)
    return img


def t_hongo():
    img = new(32, 32)
    d = ImageDraw.Draw(img)
    rect(img, 14, 24, 17, 31, 4)
    rect(img, 17, 24, 17, 31, 3)
    d.pieslice([8, 13, 23, 29], 180, 360, fill=PAL[13])
    for (x, y) in ((12, 18), (16, 16), (19, 19)):
        px(img, x, y, 4)
    return img


def t_enredadera():
    img = new(32, 32)
    for y in range(0, 26):
        x = 16 + int(2 * math.sin(y / 3.0))
        px(img, x, y, 5)
        px(img, x + 1, y, 5)
        if y % 6 == 3:
            rect(img, x + 2, y, x + 4, y + 1, 6)
            px(img, x + 3, y, 7)
            rect(img, x - 3, y + 2, x - 1, y + 3, 6)
    return img


TILES = [t_pasto(), t_tierra(), t_ladrillo(False), t_ladrillo(True),
         t_plataforma(), t_arbusto(), t_hongo(), t_enredadera()]
atlas = new(128, 64)
for i, t in enumerate(TILES):
    atlas.paste(t, ((i % 4) * 32, (i // 4) * 32))
guardar(atlas, "assets", "tiles", "tileset_bosque.png")


# ---------------------------------------------------------------- vfx, interfaz (niveles 5 y 7)
chispa = new(8, 8)
rect(chispa, 3, 3, 4, 4, 4)
for (x0, y0, x1, y1) in ((3, 1, 4, 2), (3, 5, 4, 6), (1, 3, 2, 4), (5, 3, 6, 4)):
    rect(chispa, x0, y0, x1, y1, 12)
for (x, y) in ((3, 0), (4, 0), (3, 7), (4, 7), (0, 3), (0, 4), (7, 3), (7, 4)):
    px(chispa, x, y, 14)
guardar(chispa, "assets", "vfx", "chispa.png")

marco = new(48, 48)
rect(marco, 0, 0, 47, 47, 0)
rect(marco, 1, 1, 46, 46, 11)
rect(marco, 1, 1, 46, 1, 12)
rect(marco, 1, 1, 1, 46, 12)
rect(marco, 1, 46, 46, 46, 9)
rect(marco, 46, 1, 46, 46, 9)
rect(marco, 5, 5, 42, 42, 0)
rect(marco, 6, 6, 41, 41, 1)
rect(marco, 6, 6, 41, 6, 2)
for (x, y) in ((3, 3), (44, 3), (3, 44), (44, 44)):
    px(marco, x, y, 12)
guardar(marco, "assets", "sprites", "ui_marco.png")

moneda = new(16, 16)
dm = ImageDraw.Draw(moneda)
dm.ellipse([1, 1, 14, 14], fill=PAL[12], outline=PAL[9])
rect(moneda, 7, 4, 8, 11, 14)
px(moneda, 4, 4, 4)
px(moneda, 4, 5, 4)
guardar(moneda, "assets", "sprites", "ui_moneda.png")

CORAZON = [
    "................",
    "....000..000....",
    "...0rrr00rrr0...",
    "..0rrwrrrrrrr0..",
    "..0rwrrrrrrrr0..",
    "..0rrrrrrrrrr0..",
    "..0rrrrrrrrrr0..",
    "...0rrrrrrrr0...",
    "....0rrrrrr0....",
    ".....0rrrr0.....",
    "......0rr0......",
    ".......00.......",
]
corazon = new(16, 16)
off = (16 - len(CORAZON)) // 2
for y, fila in enumerate(CORAZON):
    for x, ch in enumerate(fila):
        c = {"0": 0, "r": 13, "w": 4}.get(ch)
        if c is not None:
            px(corazon, x, y + off, c)
guardar(corazon, "assets", "sprites", "ui_corazon.png")


# ---------------------------------------------------------------- nivel (mapa de texto)
W, H = 48, 12
suelo = [["."] * W for _ in range(H)]
for x in range(W):
    suelo[9][x] = "G"
    suelo[10][x] = "D"
    suelo[11][x] = "D"
for x in (13, 14, 29, 30):
    for y in range(9, 12):
        suelo[y][x] = "."
for y in range(0, 9):
    suelo[y][0] = "B"
    suelo[y][47] = "B"
for (x, y) in ((18, 8), (19, 8), (36, 8), (37, 8), (37, 7)):
    suelo[y][x] = "M"
for x in list(range(21, 25)):
    suelo[6][x] = "P"
for x in (8, 9, 10):
    suelo[7][x] = "P"

deco = [["."] * W for _ in range(H)]
for x in (4, 25, 33, 41):
    deco[8][x] = "b"
for x in (6, 27, 39):
    deco[8][x] = "m"
for (x, y) in ((21, 7), (24, 7), (8, 8), (10, 8)):
    deco[y][x] = "v"

MONEDAS = [(7, 8), (9, 6), (13, 7), (14, 7), (22, 5), (23, 5), (29, 7), (30, 7), (34, 8)]


def filas(m):
    return ",\n".join('\t"%s"' % "".join(f) for f in m)


nivel_gd = '''extends Node2D
## Pinta el nivel a partir de mapas de texto (nivel 3).
## Suelo: G=pasto  D=tierra  B=ladrillo  M=ladrillo con musgo  P=plataforma (un solo sentido)
## Decoración: b=arbusto  m=hongo  v=enredadera
## Cada letra es una baldosa del atlas assets/tiles/tileset_bosque.png.
## Para repintar a mano, comente la llamada a _pintar en _ready y use el panel TileMap.

const SUELO: Array = [
%s
]

const DECORACION: Array = [
%s
]

const TILES_SUELO := {
	"G": Vector2i(0, 0),
	"D": Vector2i(1, 0),
	"B": Vector2i(2, 0),
	"M": Vector2i(3, 0),
	"P": Vector2i(0, 1),
}

const TILES_DECORACION := {
	"b": Vector2i(1, 1),
	"m": Vector2i(2, 1),
	"v": Vector2i(3, 1),
}

@onready var capa_suelo: TileMapLayer = $Suelo
@onready var capa_decoracion: TileMapLayer = $Decoracion


func _ready() -> void:
	_pintar(SUELO, TILES_SUELO, capa_suelo)
	_pintar(DECORACION, TILES_DECORACION, capa_decoracion)


func _pintar(mapa: Array, tiles: Dictionary, capa: TileMapLayer) -> void:
	for y in mapa.size():
		var fila: String = mapa[y]
		for x in fila.length():
			var letra: String = fila[x]
			if tiles.has(letra):
				capa.set_cell(Vector2i(x, y), 0, tiles[letra])
''' % (filas(suelo), filas(deco))
with open(P("scripts", "nivel.gd"), "w", encoding="utf-8") as f:
    f.write(nivel_gd)

monedas_nodos = ""
for i, (x, y) in enumerate(MONEDAS, 1):
    monedas_nodos += '\n[node name="Moneda%d" parent="Monedas" instance=ExtResource("4_mon")]\nposition = Vector2(%d, %d)\n' % (
        i, x * 32 + 16, y * 32 + 16)

main_tscn = '''[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/main.gd" id="1_main"]
[ext_resource type="PackedScene" path="res://escenas/nivel.tscn" id="2_niv"]
[ext_resource type="PackedScene" path="res://escenas/jugador.tscn" id="3_jug"]
[ext_resource type="PackedScene" path="res://escenas/moneda.tscn" id="4_mon"]
[ext_resource type="PackedScene" path="res://escenas/chispas.tscn" id="5_efe"]
[ext_resource type="PackedScene" path="res://escenas/interfaz.tscn" id="6_ui"]
[ext_resource type="Script" path="res://scripts/dialogo_npc.gd" id="7_npc"]
[ext_resource type="Texture2D" path="res://assets/sprites/guardian.png" id="8_gua"]
[ext_resource type="AudioStream" path="res://assets/audio/musica.ogg" id="9_mus"]
[ext_resource type="AudioStream" path="res://assets/audio/salto.wav" id="10_sal"]
[ext_resource type="AudioStream" path="res://assets/audio/recoger.wav" id="11_rec"]
[ext_resource type="AudioStream" path="res://assets/audio/dano.wav" id="12_dan"]

[sub_resource type="CircleShape2D" id="CircleShape2D_npc"]
radius = 48.0

[node name="Main" type="Node2D"]
script = ExtResource("1_main")

[node name="Cielo" type="CanvasLayer" parent="."]
layer = -1

[node name="Fondo" type="ColorRect" parent="Cielo"]
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
mouse_filter = 2
color = Color(0.353, 0.71, 0.839, 1)

[node name="Nivel" parent="." instance=ExtResource("2_niv")]

[node name="Monedas" type="Node2D" parent="."]
%s
[node name="Guardian" type="Area2D" parent="."]
position = Vector2(1400, 288)
script = ExtResource("7_npc")

[node name="Sprite2D" type="Sprite2D" parent="Guardian"]
position = Vector2(0, -16)
texture = ExtResource("8_gua")
flip_h = true

[node name="CollisionShape2D" type="CollisionShape2D" parent="Guardian"]
position = Vector2(0, -16)
shape = SubResource("CircleShape2D_npc")

[node name="Jugador" parent="." instance=ExtResource("3_jug")]
position = Vector2(64, 280)

[node name="Efectos" parent="." instance=ExtResource("5_efe")]

[node name="Musica" type="AudioStreamPlayer" parent="."]
stream = ExtResource("9_mus")
volume_db = -6.0
bus = &"Musica"

[node name="SfxSalto" type="AudioStreamPlayer" parent="."]
stream = ExtResource("10_sal")
bus = &"SFX"

[node name="SfxRecoger" type="AudioStreamPlayer" parent="."]
stream = ExtResource("11_rec")
bus = &"SFX"

[node name="SfxDano" type="AudioStreamPlayer" parent="."]
stream = ExtResource("12_dan")
bus = &"SFX"

[node name="Interfaz" parent="." instance=ExtResource("6_ui")]
''' % monedas_nodos
with open(P("escenas", "main.tscn"), "w", encoding="utf-8") as f:
    f.write(main_tscn)


# ---------------------------------------------------------------- texturas PBR (nivel 4)
def madera(sz=256):
    rng = np.random.default_rng(7)
    g = rng.random((sz, sz))
    for _ in range(4):
        g = (np.roll(g, 1, 1) + g + np.roll(g, -1, 1) + np.roll(g, 2, 1) + np.roll(g, -2, 1)) / 5
    g = (g + np.roll(g, 1, 0) + np.roll(g, -1, 0)) / 3
    g = (g - g.min()) / (g.max() - g.min())
    y = np.arange(sz)[:, None]
    vetas = 0.5 + 0.5 * np.sin((y + g * 40) * 0.9)
    ph = sz // 4
    tint = np.array([0.0, 0.08, -0.05, 0.04])[(np.arange(sz) // ph)][:, None]
    gap = np.broadcast_to(((np.arange(sz) % ph) < 3)[:, None], (sz, sz))
    t = np.clip(0.5 * g + 0.5 * vetas + tint, 0, 1)[..., None]
    oscuro = np.array([92, 56, 28], dtype=float)
    claro = np.array([170, 112, 60], dtype=float)
    alb = oscuro * (1 - t) + claro * t
    alb[gap] = [40, 24, 12]
    altura = 0.6 * g + 0.4 * vetas
    altura = np.where(gap, 0.0, altura)
    dx = (np.roll(altura, -1, 1) - np.roll(altura, 1, 1)) * 0.5
    dy_abajo = (np.roll(altura, -1, 0) - np.roll(altura, 1, 0)) * 0.5
    fuerza = 6.0
    nx, ny, nz = -dx * fuerza, dy_abajo * fuerza, np.ones_like(dx)  # estilo OpenGL (Y+ arriba)
    n = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    normal = np.stack([nx / n, ny / n, nz / n], -1) * 0.5 + 0.5
    rough = np.clip(0.65 + 0.25 * g + 0.25 * gap, 0, 1)
    return (Image.fromarray(alb.astype(np.uint8), "RGB"),
            Image.fromarray((normal * 255).astype(np.uint8), "RGB"),
            Image.fromarray((np.stack([rough] * 3, -1) * 255).astype(np.uint8), "RGB"))


alb_img, nor_img, rou_img = madera()
alb_img.save(P("assets", "texturas", "madera_albedo.png"))
nor_img.save(P("assets", "texturas", "madera_normal.png"))
rou_img.save(P("assets", "texturas", "madera_roughness.png"))


# ---------------------------------------------------------------- modelo 3D (nivel 4)
def construir_cofre():
    pos, nor, uv, idx = [], [], [], []

    def tri(p0, p1, p2, n, uvs):
        a = np.array(p1) - np.array(p0)
        b = np.array(p2) - np.array(p0)
        orden = [0, 1, 2] if np.dot(np.cross(a, b), n) >= 0 else [0, 2, 1]
        base = len(pos)
        for i in orden:
            pos.append(tuple(float(v) for v in (p0, p1, p2)[i]))
            nor.append(tuple(float(v) for v in n))
            uv.append(uvs[i])
        idx.extend([base, base + 1, base + 2])

    def quad(p0, p1, p2, p3, n, uvs=((0, 0), (1, 0), (1, 1), (0, 1))):
        tri(p0, p1, p2, n, [uvs[0], uvs[1], uvs[2]])
        tri(p0, p2, p3, n, [uvs[0], uvs[2], uvs[3]])

    x0, x1, y0, y1, z0, z1 = -0.5, 0.5, 0.0, 0.4, -0.3, 0.3
    quad((x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0), (1, 0, 0))
    quad((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0), (-1, 0, 0))
    quad((x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), (0, 1, 0))
    quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), (0, -1, 0))
    quad((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), (0, 0, 1))
    quad((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (0, 0, -1))
    # tapa semicilíndrica
    r, N = 0.3, 8
    arco = [(-r * math.cos(math.pi * i / N), y1 + r * math.sin(math.pi * i / N)) for i in range(N + 1)]
    for i in range(N):
        (za, ya), (zb, yb) = arco[i], arco[i + 1]
        tm = math.pi * (i + 0.5) / N
        n = (0, math.sin(tm), -math.cos(tm))
        v0, v1 = i / N, (i + 1) / N
        quad((x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb), n,
             ((0, v0), (1, v0), (1, v1), (0, v1)))
    for xs, n in ((x0, (-1, 0, 0)), (x1, (1, 0, 0))):
        for i in range(N):
            (za, ya), (zb, yb) = arco[i], arco[i + 1]
            tri((xs, y1, 0.0), (xs, ya, za), (xs, yb, zb), n,
                [((0 + 0.3) / 0.6, 0.0), ((za + 0.3) / 0.6, (ya - y1) / 0.3), ((zb + 0.3) / 0.6, (yb - y1) / 0.3)])
    return pos, nor, uv, idx


def escribir_glb(ruta, pos, nor, uv, idx):
    bp = np.array(pos, dtype="<f4").tobytes()
    bn = np.array(nor, dtype="<f4").tobytes()
    bu = np.array(uv, dtype="<f4").tobytes()
    bi = np.array(idx, dtype="<u2").tobytes()
    bi += b"\0" * ((4 - len(bi) % 4) % 4)
    binario = bp + bn + bu + bi
    pa = np.array(pos)
    gltf = {
        "asset": {"version": "2.0", "generator": "generar_assets.py"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"name": "Cofre3D", "children": [1]}, {"name": "Cofre", "mesh": 0}],
        "meshes": [{"name": "Cofre", "primitives": [{
            "attributes": {"POSITION": 0, "NORMAL": 1, "TEXCOORD_0": 2}, "indices": 3, "material": 0}]}],
        "materials": [{"name": "Madera", "pbrMetallicRoughness": {
            "baseColorFactor": [0.6, 0.4, 0.2, 1.0], "metallicFactor": 0.0, "roughnessFactor": 0.8}}],
        "buffers": [{"byteLength": len(binario)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(bp), "target": 34962},
            {"buffer": 0, "byteOffset": len(bp), "byteLength": len(bn), "target": 34962},
            {"buffer": 0, "byteOffset": len(bp) + len(bn), "byteLength": len(bu), "target": 34962},
            {"buffer": 0, "byteOffset": len(bp) + len(bn) + len(bu), "byteLength": len(idx) * 2, "target": 34963},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(pos), "type": "VEC3",
             "min": [float(v) for v in pa.min(0)], "max": [float(v) for v in pa.max(0)]},
            {"bufferView": 1, "componentType": 5126, "count": len(nor), "type": "VEC3"},
            {"bufferView": 2, "componentType": 5126, "count": len(uv), "type": "VEC2"},
            {"bufferView": 3, "componentType": 5123, "count": len(idx), "type": "SCALAR"},
        ],
    }
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(binario)
    with open(ruta, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total))
        f.write(struct.pack("<I4s", len(js), b"JSON") + js)
        f.write(struct.pack("<I4s", len(binario), b"BIN\0") + binario)


cofre = construir_cofre()
escribir_glb(P("assets", "modelos", "cofre.glb"), *cofre)


def render_cofre(pos, nor, idx, tam=420):
    yaw, pitch = math.radians(35), math.radians(22)
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)

    def rot(v):
        x, y, z = v
        x1, z1 = x * cy + z * sy, -x * sy + z * cy
        return x1, y * cp - z1 * sp, y * sp + z1 * cp

    luz = np.array([0.4, 0.8, 0.5])
    luz /= np.linalg.norm(luz)
    base = np.array([170, 112, 60], dtype=float)
    triangulos = []
    for i in range(0, len(idx), 3):
        vs = [rot(pos[j]) for j in idx[i:i + 3]]
        n = np.array(rot(nor[idx[i]]))
        prof = sum(v[2] for v in vs) / 3
        brillo = 0.35 + 0.65 * max(0.0, float(np.dot(n, luz)))
        triangulos.append((prof, vs, tuple(int(c) for c in np.clip(base * brillo, 0, 255))))
    triangulos.sort(key=lambda t: t[0])
    img = Image.new("RGB", (tam, tam), PAL[15][:3])
    d = ImageDraw.Draw(img)
    esc = tam * 0.55
    for _, vs, c in triangulos:
        d.polygon([(tam / 2 + v[0] * esc, tam * 0.68 - v[1] * esc) for v in vs], fill=c)
    return img


# ---------------------------------------------------------------- audio (nivel 6)
SR = 44100


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def onda_cuadrada(f, n, duty=0.5):
    ph = (np.arange(n) / SR * f) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def onda_triangular(f, n):
    ph = (np.arange(n) / SR * f) % 1.0
    return 4 * np.abs(ph - 0.5) - 1


def poner_nota(buf, inicio_s, dur_s, nota, tipo, vol, decay=2.5):
    n = int(dur_s * SR * 0.92)
    i0 = int(inicio_s * SR)
    if i0 + n > len(buf):
        n = len(buf) - i0
    f = midi(nota)
    onda = onda_cuadrada(f, n, 0.25) if tipo == "cuadrada" else onda_triangular(f, n)
    t = np.arange(n) / SR
    env = np.exp(-decay * t / dur_s)
    ataque = min(n, int(0.004 * SR))
    env[:ataque] *= np.linspace(0, 1, ataque)
    rel = min(n, int(0.01 * SR))
    env[-rel:] *= np.linspace(1, 0, rel)
    buf[i0:i0 + n] += onda * env * vol


def componer_musica():
    rng = np.random.default_rng(3)
    beat = 0.5
    corchea = beat / 2
    compases = 8
    total = int(compases * 4 * beat * SR)
    buf = np.zeros(total)
    raices = [48, 43, 45, 41, 48, 43, 41, 43]
    melodia = [
        [72, 76, 79, 76, 72, 76, 79, 84],
        [71, 74, 79, 74, 71, 74, 79, 83],
        [69, 72, 76, 72, 69, 72, 76, 81],
        [69, 72, 77, 72, 69, 72, 77, 81],
        [72, 79, 76, 79, 72, 79, 76, 84],
        [71, 79, 74, 79, 71, 79, 74, 83],
        [72, 77, 81, 77, 72, 77, 81, 84],
        [74, 71, 74, 79, 83, 79, 74, 71],
    ]
    for c in range(compases):
        t0 = c * 4 * beat
        r = raices[c]
        bajo = [r, r, r + 7, r, r, r, r + 7, r + 12]
        for i in range(8):
            poner_nota(buf, t0 + i * corchea, corchea, melodia[c][i], "cuadrada", 0.20, decay=2.0)
            poner_nota(buf, t0 + i * corchea, corchea, bajo[i], "triangular", 0.38, decay=1.2)
        for b in (0, 2):  # bombo
            n = int(0.14 * SR)
            i0 = int((t0 + b * beat) * SR)
            t = np.arange(n) / SR
            f = 130 * (45 / 130) ** (t / 0.14)
            kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-18 * t) * 0.45
            buf[i0:i0 + n] += kick
        for b in (1, 3):  # caja
            n = int(0.10 * SR)
            i0 = int((t0 + b * beat) * SR)
            t = np.arange(n) / SR
            buf[i0:i0 + n] += (rng.random(n) * 2 - 1) * np.exp(-30 * t) * 0.16
        for i in range(8):  # platillo en los contratiempos
            if i % 2 == 1:
                n = int(0.03 * SR)
                i0 = int((t0 + i * corchea) * SR)
                ruido = np.diff(rng.random(n + 1) * 2 - 1)
                buf[i0:i0 + n] += ruido * np.linspace(1, 0, n) * 0.07
    return buf


def a_int16(onda, pico=0.85):
    onda = onda / max(1e-9, np.max(np.abs(onda))) * pico
    return (onda * 32767).astype(np.int16)


def guardar_wav(ruta, onda16):
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(onda16.tobytes())


def barrido(f0, f1, dur, duty=0.5, vol=0.6, forma="cuadrada"):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    ph = (np.cumsum(f) / SR) % 1.0
    onda = np.where(ph < duty, 1.0, -1.0) if forma == "cuadrada" else 2 * ph - 1
    env = (1 - t / dur) ** 1.5
    env[: int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    return onda * env * vol


musica = componer_musica()
musica16 = a_int16(musica)
tmp_wav = P("assets", "audio", "_musica_tmp.wav")
guardar_wav(tmp_wav, musica16)
ruta_ogg = P("assets", "audio", "musica.ogg")
for codec in (["-c:a", "libvorbis", "-q:a", "5"], ["-c:a", "vorbis", "-strict", "-2", "-b:a", "128k"]):
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_wav] + codec + [ruta_ogg])
    if r.returncode == 0:
        break
os.remove(tmp_wav)

salto = barrido(280, 720, 0.22, duty=0.5, vol=0.6)
recoger = np.concatenate([barrido(988, 988, 0.07, duty=0.25, vol=0.6), barrido(1319, 1319, 0.22, duty=0.25, vol=0.6)])
n_d = int(0.38 * SR)
t_d = np.arange(n_d) / SR
dano = (np.random.default_rng(5).random(n_d) * 2 - 1) * (1 - t_d / 0.38) ** 2 * 0.5 + barrido(420, 70, 0.38, forma="sierra", vol=0.5)
guardar_wav(P("assets", "audio", "salto.wav"), a_int16(salto, 0.8))
guardar_wav(P("assets", "audio", "recoger.wav"), a_int16(recoger, 0.8))
guardar_wav(P("assets", "audio", "dano.wav"), a_int16(dano, 0.8))


# ---------------------------------------------------------------- previews (docs/capturas/previews)
def fuente(tam):
    try:
        return ImageFont.load_default(size=tam)
    except TypeError:
        return ImageFont.load_default()


def ninepatch(src, m, w, h):
    out = new(w, h)
    sw_, sh_ = src.size
    xs = [(0, m, 0, m), (m, sw_ - m, m, w - m), (sw_ - m, sw_, w - m, w)]
    ys = [(0, m, 0, m), (m, sh_ - m, m, h - m), (sh_ - m, sh_, h - m, h)]
    for (sx0, sx1, dx0, dx1) in xs:
        for (sy0, sy1, dy0, dy1) in ys:
            parte = src.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.NEAREST)
            out.paste(parte, (dx0, dy0))
    return out


PV = ("docs", "capturas", "previews")
# nivel 1
img = Image.new("RGB", (512, 80), PAL[0][:3])
img.paste(sw.convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)
d.text((8, 44), "Paleta de 16 colores (docs/paleta.png)", fill=PAL[4][:3], font=fuente(14))
img.save(P(*PV, "nivel1_paleta.png"))

# nivel 2
img = Image.new("RGB", (1024, 190), PAL[15][:3])
img.paste(escalar(hoja, 4).convert("RGB"), (0, 8))
d = ImageDraw.Draw(img)
d.text((8, 144), "quieto (cuadros 0-3)", fill=PAL[0][:3], font=fuente(16))
d.text((520, 144), "caminar (cuadros 4-7)", fill=PAL[0][:3], font=fuente(16))
img.save(P(*PV, "nivel2_personaje.png"))

# nivel 3
mundo = new(W * 32, H * 32)
for y in range(H):
    for x in range(W):
        for mapa, tabla in ((deco, {"b": 5, "m": 6, "v": 7}),
                            (suelo, {"G": 0, "D": 1, "B": 2, "M": 3, "P": 4})):
            ch = mapa[y][x]
            if ch in tabla:
                mundo.alpha_composite(TILES[tabla[ch]], (x * 32, y * 32))
for (x, y) in MONEDAS:
    mundo.alpha_composite(moneda, (x * 32 + 8, y * 32 + 8))
mundo.alpha_composite(personaje(0), (64 - 16, 288 - 32))
mundo.alpha_composite(guardian().transpose(Image.FLIP_LEFT_RIGHT), (1400 - 16, 288 - 32))
fondo = Image.new("RGBA", mundo.size, PAL[15])
fondo.alpha_composite(mundo)
fondo.convert("RGB").save(P(*PV, "nivel3_nivel.png"))

# nivel 4
hoja3d = Image.new("RGB", (256 * 3 + 20 * 4 + 420, 440), (30, 30, 36))
for i, im in enumerate((alb_img, nor_img, rou_img)):
    hoja3d.paste(im, (20 + i * 276, 20))
d = ImageDraw.Draw(hoja3d)
for i, nom in enumerate(("albedo", "normal (OpenGL)", "roughness")):
    d.text((20 + i * 276, 290), nom, fill=(230, 230, 230), font=fuente(16))
hoja3d.paste(render_cofre(cofre[0], cofre[1], cofre[3]), (20 + 3 * 276 - 20, 10))
d.text((20, 330), "Vista previa plana del cofre.glb (no es una captura de Godot)", fill=(230, 230, 230), font=fuente(14))
hoja3d.save(P(*PV, "nivel4_modelo_pbr.png"))

# nivel 5
rng = random.Random(11)
img = Image.new("RGBA", (400, 220), PAL[15])
for _ in range(32):
    ang = math.radians(-90 + rng.uniform(-30, 30))
    v = rng.uniform(80, 160)
    t = 0.3
    x = 200 + math.cos(ang) * v * t
    y = 190 + math.sin(ang) * v * t + 0.5 * 300 * t * t
    img.alpha_composite(escalar(chispa, 2), (int(x) - 8, int(y) - 8))
img.convert("RGB").save(P(*PV, "nivel5_chispas.png"))

# nivel 6
img = Image.new("RGB", (900, 340), (24, 26, 36))
d = ImageDraw.Draw(img)
series = [("musica.ogg (16 s, bucle)", musica), ("salto.wav", salto), ("recoger.wav", recoger), ("dano.wav", dano)]
for i, (nombre, onda) in enumerate(series):
    y0, alto = 10 + i * 82, 70
    d.text((8, y0), nombre, fill=(230, 230, 230), font=fuente(13))
    bloques = np.array_split(onda, 860)
    for x, b in enumerate(bloques):
        if len(b):
            a = float(np.max(np.abs(b)))
            m = a / max(1e-9, float(np.max(np.abs(onda)))) * (alto / 2 - 8)
            d.line([(20 + x, y0 + 36 - m), (20 + x, y0 + 36 + m)], fill=PAL[12][:3])
img.save(P(*PV, "nivel6_audio_ondas.png"))

# nivel 7
img = Image.new("RGBA", (800, 300), PAL[15])
img.alpha_composite(escalar(moneda, 2), (16, 12))
d = ImageDraw.Draw(img)
d.text((56, 18), "Monedas: 3", fill=PAL[0], font=fuente(20))
img.alpha_composite(ninepatch(marco, 12, 768, 140), (16, 150))
d = ImageDraw.Draw(img)
d.text((40, 166), "Guardián: ¡Alto ahí, viajero! ¿Qué te trae al bosque?", fill=PAL[4], font=fuente(20))
for i, txt in enumerate(("Busco el tesoro del bosque", "Solo estoy explorando")):
    d.rectangle([40, 204 + i * 38, 360, 236 + i * 38], fill=PAL[2], outline=PAL[0])
    d.text((50, 210 + i * 38), txt, fill=PAL[4], font=fuente(18))
img.convert("RGB").save(P(*PV, "nivel7_interfaz.png"))

# ---------------------------------------------------------------- referencias de estilo (nivel 1)
objetos = new(48, 16)
objetos.alpha_composite(moneda, (0, 0))
objetos.alpha_composite(corazon, (16, 0))
objetos.alpha_composite(escalar(chispa, 1), (36, 4))
refs = {
    "ref1_personaje": escalar(personaje(4), 10),
    "ref2_guardian": escalar(guardian(), 10),
    "ref3_baldosas": escalar(atlas, 4),
    "ref4_objetos": escalar(objetos, 10),
    "ref5_interfaz": ninepatch(marco, 12, 480, 160),
}
for nombre, im in refs.items():
    base = Image.new("RGBA", im.size, PAL[15] if nombre == "ref3_baldosas" else PAL[1])
    base.alpha_composite(im)
    base.convert("RGB").save(P("docs", "referencias", nombre + ".png"))

print("Listo:", ROOT)
