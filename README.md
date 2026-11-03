# IDRISI — Laman Produk

Laman produk gaya poster untuk **Tamara Khall Ajwa** & **Satunjang**: kad krim atas latar coklat kurma & hijau sage, tajuk condensed gergasi, tepi kertas koyak, botol atas podium, padanan keperluan → produk, dan set lengkap.

- `index.html` — laman utama
- `assets/img/` — gambar produk (latar dibuang)
- `assets/app.js` — **isi pautan jualan dalam objek `LINKS`** (WhatsApp, Shopee, TikTok, Lazada); juga penukar pandangan botol & padanan tag
- `assets/style.css` — token warna & fon di bahagian `:root`
- `assets/ad/presenter.png` — gambar presenter dalam hero

## Deploy
GitHub Pages via `.github/workflows/pages.yml` (auto bila push ke `main`).
Sekali sahaja: **Settings → Pages → Source: GitHub Actions**.

## Video iklan 30s (`ad/`)
- `ad/render.py` — render iklan 9:16 (1080x1920) guna gambar produk + presenter.
- Tambah suara: muat turun voiceover ElevenLabs ke `ad/vo.mp3`, kemudian
  `AUDIO=ad/vo.mp3 python3 ad/render.py`. Laras masa babak (`S`, `CAPS`) jika perlu.
