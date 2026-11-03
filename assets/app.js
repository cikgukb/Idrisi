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

  /* --- contact buttons --- */
  const labels = { whatsapp: "WhatsApp", shopee: "Shopee", tiktok: "TikTok Shop", lazada: "Lazada" };
  const box = document.getElementById("contact-actions");
  let any = false;
  for (const k of Object.keys(labels)) {
    if (!LINKS[k]) continue;
    any = true;
    const a = Object.assign(document.createElement("a"), { href: LINKS[k], target: "_blank", rel: "noopener", className: "btn" + (any && box.children.length ? " btn-ghost" : ""), textContent: labels[k] });
    box.appendChild(a);
  }
  if (!any) box.innerHTML = '<span class="btn btn-ghost" aria-disabled="true">Pautan tempahan akan datang</span>';
  document.querySelectorAll("[data-buy]").forEach(a => {
    const url = LINKS[a.dataset.buy] || LINKS.whatsapp;
    if (url) { a.href = url; a.target = "_blank"; a.rel = "noopener"; }
  });

  /* --- reveal on scroll --- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { threshold: 0.15 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  /* --- number counters --- */
  const countUp = el => {
    const end = parseFloat(el.dataset.count), dec = (el.dataset.count.split(".")[1] || "").length;
    if (reduce || end === 0) { el.textContent = end.toFixed(dec); return; }
    const t0 = performance.now(), dur = 1100;
    const tick = t => {
      const p = Math.min(1, (t - t0) / dur), v = end * (1 - Math.pow(1 - p, 3));
      el.textContent = v.toFixed(dec);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  /* --- scroll stories: step activation swaps the sticky bottle --- */
  document.querySelectorAll("[data-story]").forEach(story => {
    const imgs = story.querySelectorAll("[data-step-img]");
    const dots = story.querySelectorAll(".story-dots i");
    const steps = story.querySelectorAll(".step");
    const setStep = i => {
      imgs.forEach(im => im.classList.toggle("is-active", +im.dataset.stepImg === i));
      dots.forEach((d, j) => d.classList.toggle("on", j === i));
    };
    const so = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      const i = +e.target.dataset.step;
      steps.forEach(s => s.classList.toggle("is-active", s === e.target));
      setStep(i);
      e.target.querySelectorAll("[data-count]:not([data-done])").forEach(n => { n.dataset.done = 1; countUp(n); });
    }), { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach(s => so.observe(s));
    steps[0].classList.add("is-active");
  });

  /* --- scroll-linked transforms (progress bar, hero parallax, ring spin) --- */
  const bar = document.getElementById("progress-bar");
  const nav = document.querySelector(".nav");
  const hero = document.getElementById("hero-bottles");
  const rings = [...document.querySelectorAll("[data-story]")].map(s => [s, s.querySelector(".stage-ring")]);
  let ticking = false;
  const onScroll = () => {
    const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${h > 0 ? y / h : 0})`;
    nav.classList.toggle("solid", y > 40);
    if (!reduce) {
      if (y < innerHeight * 1.2) hero.style.transform = `translateY(${y * 0.25}px) scale(${1 - y / innerHeight * 0.12})`;
      rings.forEach(([s, r]) => {
        const rect = s.getBoundingClientRect();
        const p = Math.min(1, Math.max(0, -rect.top / (rect.height - innerHeight)));
        r.style.setProperty("--rot", `${p * 270}deg`);
        r.style.setProperty("--sc", (0.9 + p * 0.15).toFixed(3));
      });
    }
    ticking = false;
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener("resize", onScroll);
  onScroll();
})();
