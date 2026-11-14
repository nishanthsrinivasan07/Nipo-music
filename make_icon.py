"""Generates the original NIPO MUSIC icon (pure Pillow, no external art)."""
from PIL import Image, ImageDraw
import os
S = 1024
os.makedirs("assets/icon", exist_ok=True)

def gradient(size):
    img = Image.new("RGB", (size, size))
    px = img.load()
    c1, c2 = (124, 92, 255), (255, 79, 154)
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size - 2)
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return img

def glyph(size, scale=1.0):
    """An 'N' with a note-head at the foot of the right stem."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = int(size * 0.11 * scale)
    L, R = size * (0.5 - 0.17 * scale), size * (0.5 + 0.17 * scale)
    T, B = size * (0.5 - 0.22 * scale), size * (0.5 + 0.22 * scale)
    white = (255, 255, 255, 255)
    d.line([(L, B), (L, T)], fill=white, width=w)
    d.line([(L, T), (R, B)], fill=white, width=w)
    d.line([(R, B), (R, T + (B - T) * 0.12)], fill=white, width=w)
    for cx, cy in [(L, B), (L, T), (R, B), (R, T + (B - T) * 0.12)]:
        d.ellipse([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], fill=white)
    return layer

bg = gradient(S)
bg.save("assets/icon/icon_bg.png")
glyph(S, 0.8).save("assets/icon/icon_fg.png")
full = bg.convert("RGBA")
full.alpha_composite(glyph(S, 1.0))
full.save("assets/icon/icon.png")
