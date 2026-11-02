# IDRISI — Laman Produk

Laman portfolio interaktif (scroll) untuk **Tamara Khall Ajwa** & **Satunjang**.

- `index.html` — laman utama
- `assets/img/` — gambar produk (latar dibuang)
- `assets/app.js` — **isi pautan jualan dalam objek `LINKS`** (WhatsApp, Shopee, TikTok, Lazada)

## Deploy
GitHub Pages via `.github/workflows/pages.yml` (auto bila push ke `main`).
Sekali sahaja: **Settings → Pages → Source: GitHub Actions**.

## Video iklan 30s (`ad/`)
- `ad/render.py` — render iklan 9:16 (1080x1920) guna gambar produk + presenter.
- Tambah suara: muat turun voiceover ElevenLabs ke `ad/vo.mp3`, kemudian
  `AUDIO=ad/vo.mp3 python3 ad/render.py`. Laras masa babak (`S`, `CAPS`) jika perlu.
