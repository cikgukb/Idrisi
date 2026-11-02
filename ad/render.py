"""IDRISI 30s UGC/TV ad — 1080x1920 (9:16), 25fps.

Guna:
  python ad/render.py                     # render senyap (tiada vo.mp3)
  AUDIO=ad/vo.mp3 python ad/render.py     # render dengan voiceover
  PREVIEW="2 7 14 20 27" python ad/render.py   # simpan frame pratonton sahaja
Fon Poppins dijangka di ad/fonts/.
"""
import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, *p)
W, H, FPS, DUR = 1080, 1920, 25, 30.0
OUT = os.environ.get("OUT", A("ad", "idrisi-ad-30s.mp4"))
AUDIO = os.environ.get("AUDIO")
F = lambda w, s: ImageFont.truetype(A("ad", "fonts", f"Poppins-{w}.ttf"), s)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

GOLD, GOLD2, AMBER, CREAM, RED = (216, 166, 74), (240, 201, 119), (217, 133, 59), (244, 237, 226), (200, 35, 44)
BG = (13, 11, 9)

# ---------- timeline (saat). Laras ikut timings.py selepas ada vo.mp3 ----------
S = dict(hook=0.0, tamara=3.6, satunjang=10.4, dose=17.2, cta=21.6)
CAPS = [  # (mula, tamat, teks)
    (0.2, 3.5, "Korang! Ni dua botol yang SAYA minum setiap hari."),
    (3.7, 5.6, "Yang pertama, TAMARA."),
    (5.6, 8.2, "Ekstrak kurma Ajwa, ditapai secara semula jadi."),
    (8.2, 10.3, "100% kurma Ajwa. Tanpa pengawet, tanpa bahan tambahan."),
    (10.5, 12.3, "Yang kedua, SATUNJANG."),
    (12.3, 15.2, "Minuman botani kurma merah, dang gui & dang shen."),
    (15.2, 17.1, "Khas untuk lelaki dewasa."),
    (17.3, 21.4, "Cukup 10–15ml setiap kali minum. Senang je!"),
    (21.7, 24.4, "Nak cuba? Layari website IDRISI sekarang."),
    (24.4, 27.4, "Link ada kat bawah!"),
]
URL = "cikgukb.github.io/idrisi"

# ---------- helpers ----------
clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d)
def ease_out(x): return 1 - (1 - x) ** 3
def back(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def load(p, h):
    im = Image.open(p).convert("RGBA")
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

def paste(base, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0 or scale <= 0.01: return
    if scale != 1.0:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))

def shadowed(im, blur=28, off=30, op=150):
    pad = blur * 3
    c = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2 + off), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, op)); sh.putalpha(im.getchannel("A").point(lambda v: v * op // 255))
    c.alpha_composite(sh, (pad, pad + off)); c = c.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(im, (pad, pad)); return c

def radial(color, cx, cy, r, strength=0.55):
    g = Image.new("L", (W // 4, H // 4), 0); d = ImageDraw.Draw(g)
    for i in range(60, 0, -1):
        rr = r / 4 * i / 60; v = int(255 * strength * (1 - i / 60) ** 1.6)
        d.ellipse((cx / 4 - rr, cy / 4 - rr, cx / 4 + rr, cy / 4 + rr), fill=v)
    g = g.filter(ImageFilter.GaussianBlur(12)).resize((W, H), Image.BILINEAR)
    base = Image.new("RGBA", (W, H), BG + (255,)); col = Image.new("RGBA", (W, H), color + (255,))
    return Image.composite(col, base, g)

def text_c(d, xy, s, font, fill, anchor="mm", **kw): d.text(xy, s, font=font, fill=fill, anchor=anchor, **kw)

def wrap(s, font, maxw, d):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def ring(base, cx, cy, r, color, ang, alpha):
    if alpha <= 0: return
    L = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(L)
    a = int(110 * alpha)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color + (a,), width=3)
    px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
    d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=color + (int(255 * alpha),))
    base.alpha_composite(L)

def chip(base, cx, cy, s, color, p):
    if p <= 0: return
    f = F("SemiBold", 34); d0 = ImageDraw.Draw(base); tw = d0.textlength(s, font=f)
    w, h = int(tw + 56), 72
    L = Image.new("RGBA", (w + 4, h + 4)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((2, 2, w, h), radius=36, fill=(30, 24, 18, 230), outline=color + (255,), width=3)
    d.text(((w + 2) / 2, (h + 2) / 2), s, font=f, fill=color, anchor="mm")
    paste(base, L, cx, cy + (1 - ease_out(p)) * 40, scale=0.6 + 0.4 * back(p), alpha=clamp(p * 1.5))

def badge(base, cx, cy, scale=1.0, alpha=1.0):
    f = ImageFont.truetype(SERIF, 54); tmp = ImageDraw.Draw(base); tw = tmp.textlength("IDRISI", font=f)
    w, h = int(tw + 50), 86
    L = Image.new("RGBA", (w + 12, h + 12)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((0, 0, w + 11, h + 11), radius=12, fill=RED + (255,))
    d.rounded_rectangle((5, 5, w + 6, h + 6), radius=9, outline=(255, 255, 255, 255), width=4)
    d.text(((w + 12) / 2, (h + 12) / 2 + 2), "IDRISI", font=f, fill="white", anchor="mm")
    paste(base, L, cx, cy, scale, alpha)

def caption(base, t):
    for t0, t1, s in CAPS:
        if t0 <= t < t1:
            a = min(prog(t, t0, 0.15), 1 - prog(t, t1 - 0.12, 0.12))
            f = F("Bold", 50); d = ImageDraw.Draw(base)
            lines = wrap(s, f, W - 200, d); lh = 68
            bh = lh * len(lines) + 44; y0 = 1540
            L = Image.new("RGBA", (W, H)); dl = ImageDraw.Draw(L)
            dl.rounded_rectangle((70, y0, W - 70, y0 + bh), radius=26, fill=(0, 0, 0, int(165 * a)))
            for i, ln in enumerate(lines):
                # highlight product names
                col = GOLD2 if ("TAMARA" in ln or "IDRISI" in ln) else (AMBER if "SATUNJANG" in ln else CREAM)
                dl.text((W / 2, y0 + 22 + lh * i + lh / 2), ln, font=f, fill=col + (int(255 * a),), anchor="mm")
            base.alpha_composite(L)

# ---------- assets ----------
IMG = lambda n: A("assets", "img", n + ".webp")
pres = shadowed(load(A("assets", "ad", "presenter.png"), 1150), 24, 20, 120)
tam_big = shadowed(load(IMG("tamara-front"), 1050))
tam_mid = shadowed(load(IMG("tamara-front"), 820))
tam_back = shadowed(load(IMG("tamara-story"), 760))
sat_big = shadowed(load(IMG("satunjang-front"), 1000))
sat_mid = shadowed(load(IMG("satunjang-front"), 700))
sat_info = shadowed(load(IMG("satunjang-info"), 640))
BG_GOLD = radial(GOLD, W / 2, 760, 900, 0.45)
BG_AMBER = radial(AMBER, W / 2, 760, 900, 0.45)
BG_MIX = radial((180, 120, 60), W / 2, 820, 1000, 0.40)

def scene_hook(f, t):
    p = prog(t, 0.1, 0.7)
    f.alpha_composite(BG_MIX)
    d = ImageDraw.Draw(f)
    a = ease_out(prog(t, 0.2, 0.5))
    text_c(d, (W / 2, 210 - (1 - a) * 40), "KORANG!", F("ExtraBold", 132), GOLD2 + (int(255 * a),))
    text_c(d, (W / 2, 330), "rutin harian saya", F("Medium", 46), CREAM + (int(255 * ease_out(prog(t, 0.6, 0.5))),))
    bob = math.sin(t * 2.4) * 8
    paste(f, tam_mid, 330, 980 + bob, scale=back(prog(t, 0.9, 0.6)) * 0.95, rot=4)
    paste(f, sat_mid, 560, 1030 - bob, scale=back(prog(t, 1.2, 0.6)) * 0.95, rot=-5)
    paste(f, pres, 840 + (1 - ease_out(p)) * 500, 1080 + bob * 0.6, scale=0.92)

def scene_tamara(f, t):
    f.alpha_composite(BG_GOLD); d = ImageDraw.Draw(f)
    lt = t - S["tamara"]
    ring(f, W / 2, 900, 470, GOLD, lt * 0.9 - 1.5, ease_out(prog(lt, 0, 0.6)))
    p = ease_out(prog(lt, 0, 0.8))
    if lt < 4.2:
        paste(f, tam_big, W / 2, 990 + (1 - p) * 300 + math.sin(t * 2) * 10, scale=0.85 + 0.15 * p, alpha=p)
    else:  # flip to label/back
        q = ease_out(prog(lt, 4.2, 0.6))
        paste(f, tam_big, W / 2 - q * 520, 920, alpha=1 - q)
        paste(f, tam_back, W / 2 + (1 - q) * 520, 900 + math.sin(t * 2) * 10, alpha=q, scale=1.15)
    a = ease_out(prog(lt, 0.2, 0.5))
    text_c(d, (W / 2, 180), "KHALL AJWA", F("SemiBold", 36), GOLD + (int(255 * a),))
    text_c(d, (W / 2, 280 - (1 - a) * 30), "TAMARA", ImageFont.truetype(SERIF, 140), GOLD2 + (int(255 * a),))
    chip(f, 280, 1420, "100% Kurma Ajwa", GOLD2, prog(lt, 4.5, 0.5))
    chip(f, 800, 1420, "Tanpa Pengawet", GOLD2, prog(lt, 4.9, 0.5))
    chip(f, W / 2, 400, "Pure Fermented Ajwa Extract", GOLD, prog(lt, 1.8, 0.5))

def scene_satunjang(f, t):
    f.alpha_composite(BG_AMBER); d = ImageDraw.Draw(f)
    lt = t - S["satunjang"]
    ring(f, W / 2, 900, 470, AMBER, -lt * 0.9, ease_out(prog(lt, 0, 0.6)))
    p = ease_out(prog(lt, 0, 0.8))
    if lt < 2.2:
        paste(f, sat_big, W / 2, 940 + (1 - p) * 300 + math.sin(t * 2) * 10, scale=0.85 + 0.15 * p, alpha=p)
    else:
        q = ease_out(prog(lt, 2.2, 0.6))
        paste(f, sat_big, W / 2 - q * 260, 960, alpha=1 - q * 0.0, scale=1 - 0.35 * q)
        # ingredient bars
        bars = [("Kurma merah", 35), ("Dang Shen", 12), ("Dang Gui", 10)]
        L = Image.new("RGBA", (W, H)); dl = ImageDraw.Draw(L)
        for i, (nm, pc) in enumerate(bars):
            bp = ease_out(prog(lt, 2.6 + i * 0.35, 0.8)); y = 760 + i * 170
            if bp <= 0: continue
            al = int(255 * clamp(bp * 2))
            dl.text((560, y), nm, font=F("SemiBold", 40), fill=CREAM + (al,), anchor="lm")
            dl.rounded_rectangle((560, y + 40, 980, y + 64), radius=12, fill=(255, 255, 255, int(40 * bp)))
            dl.rounded_rectangle((560, y + 40, 560 + max(24, 420 * pc / 40 * bp), y + 64), radius=12, fill=AMBER + (al,))
            dl.text((980, y), f"{round(pc * bp)}%", font=F("Bold", 44), fill=(242, 176, 108, al), anchor="rm")
        f.alpha_composite(L)
    a = ease_out(prog(lt, 0.2, 0.5))
    text_c(d, (W / 2, 180), "MINUMAN BOTANI", F("SemiBold", 36), AMBER + (int(255 * a),))
    text_c(d, (W / 2, 280 - (1 - a) * 30), "SATUNJANG", ImageFont.truetype(SERIF, 118), (242, 176, 108, int(255 * a)))
    chip(f, W / 2, 1420, "Khas lelaki dewasa · MeSTI · GMP", (242, 176, 108), prog(lt, 4.8, 0.5))

def scene_dose(f, t):
    f.alpha_composite(BG_MIX); d = ImageDraw.Draw(f)
    lt = t - S["dose"]; bob = math.sin(t * 2.4) * 8
    paste(f, tam_mid, 330, 1010 + bob, scale=back(prog(lt, 0, 0.6)), rot=3)
    paste(f, sat_mid, 750, 1050 - bob, scale=back(prog(lt, 0.2, 0.6)), rot=-3)
    a = ease_out(prog(lt, 0.3, 0.5))
    n = 10 + round(5 * ease_out(prog(lt, 0.8, 1.0)))
    text_c(d, (W / 2, 300), f"10–{n}ml", F("ExtraBold", 170), GOLD2 + (int(255 * a),))
    text_c(d, (W / 2, 450), "setiap kali minum", F("Medium", 52), CREAM + (int(255 * a),))
    chip(f, W / 2, 560, "Senang je! ✓".replace("✓", ""), GOLD2, prog(lt, 2.2, 0.5))

def scene_cta(f, t):
    f.alpha_composite(BG_GOLD); d = ImageDraw.Draw(f)
    lt = t - S["cta"]; bob = math.sin(t * 2.4) * 8
    badge(f, W / 2, 170, scale=back(prog(lt, 0, 0.5)))
    paste(f, tam_mid, 230, 930 + bob, scale=0.85 * back(prog(lt, 0.2, 0.5)), rot=4)
    paste(f, sat_mid, 440, 990 - bob, scale=0.85 * back(prog(lt, 0.4, 0.5)), rot=-4)
    paste(f, pres, 820 + (1 - ease_out(prog(lt, 0, 0.7))) * 500, 900 + bob * 0.6, scale=0.85)
    a = ease_out(prog(lt, 0.3, 0.5))
    text_c(d, (W / 2, 300), "Nak cuba?", F("ExtraBold", 92), CREAM + (int(255 * a),))
    # button + typed URL
    bp = back(prog(lt, 1.2, 0.5))
    if bp > 0:
        L = Image.new("RGBA", (900, 230)); dl = ImageDraw.Draw(L)
        dl.rounded_rectangle((10, 10, 890, 130), radius=60, fill=GOLD + (255,))
        dl.text((450, 70), "LAYARI WEBSITE IDRISI", font=F("Bold", 50), fill=(18, 13, 7), anchor="mm")
        k = int(len(URL) * prog(lt, 1.8, 1.4)); cur = "|" if int(t * 3) % 2 == 0 and k < len(URL) else ""
        dl.text((450, 185), URL[:k] + cur, font=F("SemiBold", 46), fill=GOLD2 + (255,), anchor="mm")
        paste(f, L, W / 2, 1335, scale=bp)
    # pulse arrow after typing
    if lt > 4.0:
        y = 1460 + math.sin(t * 6) * 10
        text_c(d, (W / 2, y), "link kat bawah", F("SemiBold", 40), CREAM + (230,))

SCENES = [("hook", scene_hook), ("tamara", scene_tamara), ("satunjang", scene_satunjang), ("dose", scene_dose), ("cta", scene_cta)]

def frame(t):
    f = Image.new("RGBA", (W, H), BG + (255,))
    keys = [S[k] for k, _ in SCENES] + [DUR + 1]
    for i, (k, fn) in enumerate(SCENES):
        if keys[i] <= t < keys[i + 1]:
            fn(f, t)
            # fade transitions
            fade = max(1 - prog(t, keys[i], 0.25), prog(t, keys[i + 1] - 0.25, 0.25) if i < len(SCENES) - 1 else 0)
            if fade > 0: f.alpha_composite(Image.new("RGBA", (W, H), BG + (int(255 * fade),)))
    caption(f, t)
    if t > DUR - 0.6: f.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * prog(t, DUR - 0.6, 0.6)))))
    return f.convert("RGB")

if __name__ == "__main__":
    pv = os.environ.get("PREVIEW")
    if pv:
        for s in pv.split():
            frame(float(s)).save(A("ad", f"preview_{s}.jpg"), quality=85)
        sys.exit()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if AUDIO: cmd += ["-i", AUDIO, "-af", "adelay=200|200,apad", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-movflags", "+faststart", OUT]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        pr.stdin.write(frame(i / FPS).tobytes())
        if i % 100 == 0: print(f"{i}/{n}", flush=True)
    pr.stdin.close(); pr.wait(); print("siap", OUT)
