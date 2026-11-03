/* =========================================================
   PAUTAN JUALAN — isi kemudian (WhatsApp, Shopee, TikTok…)
   Biarkan "" untuk sembunyikan butang.
   ========================================================= */
const WA = "60184066544";
const wa = produk => `https://wa.me/${WA}?text=${encodeURIComponent("Saya berminat untuk dapatkan produk " + produk)}`;
const LINKS = {
  whatsapp: wa("Tamara / Satunjang"),
  shopee:   "",   // cth: "https://shopee.com.my/..."
  tiktok:   "",   // cth: "https://www.tiktok.com/@..."
  lazada:   "",
  // Pautan khusus untuk butang "Beli Tamara" / "Beli Satunjang"
  tamara:    wa("Tamara"),
  satunjang: wa("Satunjang")
};

(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.getElementById("year").textContent = new Date().getFullYear();

  /* --- butang hubungi (footer) --- */
  const labels = { whatsapp: "WhatsApp", shopee: "Shopee", tiktok: "TikTok Shop", lazada: "Lazada" };
  const box = document.getElementById("contact-actions");
  let any = false;
  for (const k of Object.keys(labels)) {
    if (!LINKS[k]) continue;
    const a = Object.assign(document.createElement("a"), {
      href: LINKS[k], target: "_blank", rel: "noopener",
      className: "btn" + (any ? " btn-ghost" : ""), textContent: labels[k]
    });
    box.appendChild(a);
    any = true;
  }
  if (!any) box.innerHTML = '<span class="btn btn-ghost" aria-disabled="true">Pautan tempahan akan datang</span>';

  /* --- semua butang beli: ikut LINKS, jatuh balik ke WhatsApp umum --- */
  document.querySelectorAll("[data-buy]").forEach(a => {
    const url = LINKS[a.dataset.buy] || LINKS.whatsapp;
    if (url) { a.href = url; a.target = "_blank"; a.rel = "noopener"; }
  });

  /* --- rak: tukar pandangan botol (depan / kisah / ramuan) --- */
  document.querySelectorAll(".stand").forEach(stand => {
    const imgs = stand.querySelectorAll(".bottle");
    const tabs = stand.querySelectorAll(".views button");
    tabs.forEach(t => t.addEventListener("click", () => {
      const v = t.dataset.view;
      tabs.forEach(o => o.setAttribute("aria-selected", o === t ? "true" : "false"));
      imgs.forEach(im => im.classList.toggle("is-active", im.dataset.view === v));
    }));
  });

  /* --- padanan: tag keperluan → produk --- */
  const names = { tamara: "Tamara", satunjang: "Satunjang" };
  const why = {
    tamara: "ekstrak Ajwa terfermentasi, sesuai seisi keluarga termasuk kanak-kanak 7 tahun ke atas.",
    satunjang: "minuman botani kurma merah, Dang Gui dan Dang Shen, dirumus untuk lelaki dewasa."
  };
  const tags = document.querySelectorAll("#tags .tag");
  const pick = document.getElementById("pick");
  const switchBtns = document.querySelectorAll(".switch button");
  const panels = document.querySelectorAll(".panel");
  const bottles = document.querySelectorAll(".match-bottle img");

  const select = key => {
    switchBtns.forEach(b => b.setAttribute("aria-selected", b.dataset.product === key ? "true" : "false"));
    panels.forEach(p => { const on = p.dataset.product === key; p.hidden = !on; p.classList.toggle("is-active", on); });
    bottles.forEach(b => b.classList.toggle("is-active", b.dataset.product === key));
  };

  tags.forEach(t => t.addEventListener("click", () => {
    tags.forEach(o => o.setAttribute("aria-pressed", "false"));
    t.setAttribute("aria-pressed", "true");
    const key = t.dataset.product;
    pick.innerHTML = `Untuk <strong>${t.textContent}</strong>, kami cadangkan <em>${names[key]}</em>: ${why[key]}`;
    select(key);
  }));
  switchBtns.forEach(b => b.addEventListener("click", () => {
    tags.forEach(o => o.setAttribute("aria-pressed", "false"));
    select(b.dataset.product);
  }));
  select("tamara");

  /* --- paralaks ringan untuk coretan berus di hero --- */
  if (!reduce) {
    const doodles = document.querySelectorAll(".doodle");
    let ticking = false;
    addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const y = scrollY;
        doodles.forEach((d, i) => { d.style.marginTop = (y * (0.03 + (i % 3) * 0.02)) + "px"; });
        ticking = false;
      });
    }, { passive: true });
  }
})();
