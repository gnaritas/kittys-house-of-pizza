#!/usr/bin/env python3
"""og.png 1200x630 — Kitty's House of Pizza: restored-1963-service-station theme.
Retro canopy sign on posts, candy-stripe bands, brick-oven slice mark, opening badge.
Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (23, 38, 43); PAPER = (245, 239, 225); PAPER2 = (236, 225, 202); CREAM = (250, 245, 233)
TOMATO = (194, 59, 28); TEAL = (42, 125, 116); GOLD = (217, 155, 47)

def font(path_names, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in path_names:
            p = b + n
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

serif = lambda s: font(["Palatino.ttc", "Georgia.ttf", "Times New Roman.ttf"], s)
sans = lambda s: font(["Futura.ttc", "HelveticaNeue.ttc", "Arial.ttf"], s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# paper wash — deeper toward bottom
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(PAPER[0] - int(8 * t), PAPER[1] - int(12 * t), PAPER[2] - int(22 * t)))

# faint dot field top-right (halftone corner)
for row in range(14):
    for col in range(20):
        x = 780 + col * 22 + (row % 2) * 11
        y = 66 + row * 22
        dd = max(2, 9 - row // 3)
        d.ellipse((x - dd, y - dd, x + dd, y + dd), fill=TEAL + (70,))

# candy-stripe bands, top and bottom
def stripe_band(y0, band_h, slant=34):
    step = 46
    for i in range(-band_h, W + band_h, step):
        col = [TOMATO, GOLD, CREAM][(i // step) % 3]
        pts = [(i, y0), (i + band_h * 2, y0), (i + slant + band_h * 2, y0 + band_h), (i + slant, y0 + band_h)]
        d.polygon(pts, fill=col)
stripe_band(0, 20)
stripe_band(H - 20, 20)
d.rectangle((0, 20, W, 26), fill=INK)
d.rectangle((0, H - 26, W, H - 20), fill=INK)

# left text column
d.text((84, 110), "N O W  O P E N I N G", font=sans(24), fill=TEAL)
d.text((84, 138), "Kitty's", font=serif(118), fill=INK)
d.text((88, 268), "HOUSE OF PIZZA", font=sans(44), fill=TOMATO)
d.text((88, 336), "Brick-oven pizza · House-made pastas", font=serif(32), fill=INK)
d.text((88, 378), "Bright Ice pints by the scoop", font=serif(32), fill=INK)
d.line([(88, 424), (560, 424)], fill=INK, width=4)
d.text((88, 440), "4059 5th Ave N · Central Oak Park", font=sans(24), fill=INK)
d.text((88, 466), "St. Petersburg, Florida", font=sans(24), fill=INK)

# rotated opening badge — below the text block, clear of the bottom stripe
badge_w, badge_h = 225, 70
badge = Image.new("RGBA", (badge_w + 20, badge_h + 20), (0, 0, 0, 0))
bd = ImageDraw.Draw(badge)
bd.rounded_rectangle((10, 10, 10 + badge_w, 10 + badge_h), radius=16, fill=TEAL)
bd.text((badge_w // 2 + 10, badge_h // 2 + 10 - 16), "OPENS", font=sans(21), fill=(255, 255, 255, 200), anchor="mm")
bd.text((badge_w // 2 + 10, badge_h // 2 + 10 + 11), "NOV. 17", font=sans(32), fill=(255, 255, 255, 255), anchor="mm")
badge = badge.rotate(-4, expand=True, resample=Image.BICUBIC)
bw_new, bh_new = badge.size
bx, by = 88, 604 - bh_new - 4
img.paste(badge, (bx, by), badge.convert("RGBA"))

# right: retro price sign on posts
sx, sy, sw, sh = 700, 110, 420, 330
d.rectangle((sx + 40, sy + sh, sx + 66, sy + sh + 120), fill=INK)          # left post
d.rectangle((sx + sw - 66, sy + sh, sx + sw - 40, sy + sh + 120), fill=INK) # right post
d.rectangle((sx - 6, sy - 6, sx + sw + 6, sy + sh + 6), fill=INK)           # sign frame
d.rectangle((sx, sy, sx + sw, sy + sh), fill=CREAM)
# sign inner header
d.rectangle((sx, sy, sx + sw, sy + 64), fill=INK)
d.text((sx + sw // 2, sy + 32), "Kitty's", font=serif(40), fill=GOLD, anchor="mm")
# big price-board line
d.text((sx + sw // 2, sy + 130), "BRICK-OVEN", font=sans(40), fill=INK, anchor="mm")
d.text((sx + sw // 2, sy + 182), "PIZZA", font=sans(56), fill=TOMATO, anchor="mm")
d.line([(sx + 46, sy + 224), (sx + sw - 46, sy + 224)], fill=GOLD, width=5)
d.text((sx + sw // 2, sy + 262), "· HOUSE-MADE PASTAS ·", font=sans(24), fill=INK, anchor="mm")
d.text((sx + sw // 2, sy + 300), "BRIGHT ICE PINTS", font=sans(28), fill=TEAL, anchor="mm")
# slice mark under sign
cx, cy = sx + sw // 2, sy + sh + 88
d.polygon([(cx, cy - 62), (cx + 74, cy + 58), (cx - 74, cy + 58)], fill=PAPER2, outline=INK)
d.polygon([(cx, cy - 48), (cx + 60, cy + 48), (cx - 60, cy + 48)], fill=CREAM, outline=TOMATO, width=3)
for px, py in [(-26, 22), (10, 12), (-6, 38), (24, 36)]:
    d.ellipse((cx + px - 8, cy + py - 8, cx + px + 8, cy + py + 8), fill=TOMATO)

img.save(OUT, "PNG")
print("wrote", OUT, img.size)
