"""Jana sound effect + muzik latar asli (sintesis, bebas hak cipta) untuk iklan 30s.
Output: ad/sfx.wav (SFX) dan ad/bed.wav (muzik latar). 48kHz stereo.
Masa diselaraskan dengan babak dalam ad/render.py.
"""
import os, wave, numpy as np

SR, DUR = 48000, 30.0
N = int(SR * DUR)
D = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(SR * d)) / SR

def env(n, a=0.005, r=0.2, shape=4.0):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    return e * np.exp(-np.linspace(0, shape, n)) if r is None else e * np.clip(np.linspace(1, 0, n) ** (1 / max(r, 1e-3)), 0, 1)

def lp(x, k=0.15):  # 1-pole low-pass
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y

def whoosh(d=0.55, up=True):
    n = int(SR * d); x = rng.standard_normal(n)
    k = np.linspace(0.02, 0.35, n) if up else np.linspace(0.35, 0.02, n)
    y = np.empty(n); acc = 0.0
    for i in range(n): acc += k[i] * (x[i] - acc); y[i] = acc
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return y * e * 2.2

def pop(f=520, d=0.14):
    t = t_(d); fr = f * (1 + 1.6 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 28) * 0.8

def sparkle(d=1.2):
    out = np.zeros(int(SR * d))
    for i in range(14):
        st = int(rng.uniform(0, d * 0.7) * SR); f = rng.uniform(2200, 5200); t = t_(0.35)
        s = np.sin(2 * np.pi * f * t) * np.exp(-t * 12) * 0.18
        out[st:st + len(s)] += s[: len(out) - st]
    return out

def ding(f=1318.5, d=1.4):
    t = t_(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f * 3.02 * t)) * np.exp(-t * 3.2) * 0.35

def tick(f=1800): t = t_(0.03); return np.sin(2 * np.pi * f * t) * np.exp(-t * 160) * 0.5

def key_click():
    t = t_(0.045); n = rng.standard_normal(len(t)) * np.exp(-t * 180) * 0.35
    return n + np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 220) * 0.15

def riser(d=1.0, f0=300, f1=1400):
    t = t_(d); fr = np.linspace(f0, f1, len(t))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.linspace(0, 1, len(t)) ** 2 * 0.18 + whoosh(d) * 0.3

def chime():  # CTA success: arpeggio naik
    out = np.zeros(int(SR * 1.6))
    for i, f in enumerate([783.99, 987.77, 1174.66, 1567.98]):
        s = ding(f, 1.2) * 0.8; st = int(i * 0.09 * SR); out[st:st + len(s)] += s[: len(out) - st]
    return out

sfx = np.zeros(N)
def at(sec, s, g=1.0):
    st = int(sec * SR); e = min(N, st + len(s)); sfx[st:e] += s[: e - st] * g

# hook
at(0.0, riser(0.6), 0.9); at(0.15, whoosh(0.5), 0.7)
at(0.95, pop(480), 0.8); at(1.25, pop(560), 0.8)
# tamara
at(2.95, whoosh(0.5), 0.8); at(3.3, sparkle(1.3), 1.0); at(5.0, pop(700, 0.1), 0.5)
at(8.0, whoosh(0.45, up=False), 0.6); at(8.5, pop(620), 0.7); at(10.4, pop(700), 0.7)
# satunjang
at(12.15, whoosh(0.5), 0.8); at(12.5, sparkle(1.0), 0.6)
for i in range(3): at(15.0 + i * 0.35, pop(520 + i * 120, 0.12), 0.6)
at(17.6, pop(640), 0.6)
# dose
at(18.75, whoosh(0.5), 0.8); at(19.0, pop(500), 0.7); at(19.2, pop(600), 0.7)
for i in range(5): at(19.8 + i * 0.2, tick(1500 + i * 150), 0.8)
at(20.8, ding(1318.5, 1.2), 0.9); at(22.4, pop(760, 0.1), 0.5)
# cta
at(23.05, whoosh(0.5), 0.8); at(23.3, pop(440, 0.18), 0.9); at(24.5, pop(600, 0.16), 0.9)
for i in range(len("cikgukb.github.io/idrisi")): at(25.1 + i * 1.4 / 24, key_click(), 0.9)
at(26.6, chime(), 0.9)

# ---- muzik latar: groove ringkas 104 BPM (kick, hat, bass, pad) ----
bpm = 104; beat = 60 / bpm; bed = np.zeros(N)
chords = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66), (164.81, 207.65, 246.94)]  # Am F G E
def kick():
    t = t_(0.28); fr = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9)
def hat():
    t = t_(0.05); x = rng.standard_normal(len(t)); x = x - lp(x, 0.6)
    return x * np.exp(-t * 90) * 0.18
nb = int(DUR / beat) + 1
for b in range(nb):
    s = b * beat
    st = int(s * SR)
    def add(sig, off=0.0, g=1.0):
        a = int((s + off) * SR); e = min(N, a + len(sig))
        if a < N: bed[a:e] += sig[: e - a] * g
    if b % 4 in (0, 2) or (b % 8 == 7): add(kick(), 0, 0.55)
    add(hat(), beat / 2, 0.8)
    ch = chords[(b // 4) % 4]
    if b % 4 == 0:  # pad per bar
        t = t_(beat * 4); pad = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t) for f in ch)
        add(pad * np.sin(np.linspace(0, np.pi, len(t))) ** 0.6 * 0.045)
    t = t_(beat * 0.9); add(np.sin(2 * np.pi * ch[0] / 2 * t) * np.exp(-t * 3) * 0.22)  # bass
fade = np.ones(N); fade[: int(0.6 * SR)] = np.linspace(0, 1, int(0.6 * SR)); fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
bed *= fade

def save(name, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    st = (np.stack([x, x], 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(D, name), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
save("sfx.wav", sfx); save("bed.wav", bed); print("siap sfx.wav bed.wav")
