/* ============================================================
   HitBeatRun — site settings. Edit these three values.
   ============================================================ */
const HBR = {
  // Your Fourthwall subscription / membership page (every "Let's Run" button goes here)
  FOURTHWALL_URL: 'https://hitbeatrun.com/supporters',
  // Your Fourthwall shop home (used by "Log In")
  FOURTHWALL_HOME: 'https://hitbeatrun.com',
  // Shown in the footer and used by the forms when no FORM_ENDPOINT is set
  CONTACT_EMAIL: 'info@hitbeatrun.com',
  // Optional: a Formspree / Getform / Basin URL so forms submit without opening email
  FORM_ENDPOINT: '',
};

(() => {
  const body = document.body;

  // Every "Let's Run" button goes to the Fourthwall subscription page
  document.querySelectorAll('[data-cta]').forEach(a => { a.href = HBR.FOURTHWALL_URL; });
  document.querySelectorAll('[data-fourthwall]').forEach(a => { a.href = HBR.FOURTHWALL_HOME; });
  document.querySelectorAll('[data-email]').forEach(a => {
    a.href = 'mailto:' + HBR.CONTACT_EMAIL; a.textContent = HBR.CONTACT_EMAIL;
  });

  // Mobile menu
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  burger?.addEventListener('click', () => nav.classList.toggle('open'));
  nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

  // Background videos: load + play only while on screen
  const vids = document.querySelectorAll('video[data-src]');
  const vio = new IntersectionObserver(entries => {
    entries.forEach(({ target: v, isIntersecting }) => {
      if (isIntersecting) {
        if (!v.src) v.src = v.dataset.src;
        v.play().catch(() => {});
      } else if (!v.paused) v.pause();
    });
  }, { rootMargin: '200px' });
  vids.forEach(v => vio.observe(v));

  // Hero card stack (same effect as Wix): each card slides up, grows from 88% to 100%
  // and fades its video in, landing exactly on top of the previous one; the finished
  // pile then scrolls away together.
  const cards = [...document.querySelectorAll('.stack-card')];
  if (cards.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const vidOf = cards.map(c => c.querySelector('video'));
    let ticking = false;
    const update = () => {
      ticking = false;
      const vh = innerHeight;
      cards.forEach((card, i) => {
        if (i === 0) return;
        const stickTop = parseFloat(getComputedStyle(card).top);
        const top = card.getBoundingClientRect().top;
        const p = Math.min(1, Math.max(0, 1 - (top - stickTop) / (vh - stickTop)));
        const e = 1 - Math.pow(1 - p, 3);
        card.style.transform = `scale(${0.88 + 0.12 * e})`;
        if (vidOf[i]) vidOf[i].style.opacity = Math.min(1, p * 1.6).toFixed(3);
      });
    };
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', onScroll);
    update();
  }

  // Hero: floating tags and icons drift with the mouse (desktop only)
  const heroTop = document.querySelector('.hero-top');
  if (heroTop && matchMedia('(hover: hover) and (prefers-reduced-motion: no-preference)').matches) {
    heroTop.addEventListener('mousemove', e => {
      const r = heroTop.getBoundingClientRect();
      heroTop.style.setProperty('--mx', ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      heroTop.style.setProperty('--my', ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    });
    heroTop.addEventListener('mouseleave', () => { heroTop.style.setProperty('--mx', 0); heroTop.style.setProperty('--my', 0); });
  }

  // Reveal-on-scroll and the progress bars
  const rio = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
  }, { threshold: 0.15 });
  document.querySelectorAll('.reveal, .bars').forEach(el => rio.observe(el));

  // Highlight "Speakers" while the athlete section is on screen
  const speakers = document.querySelector('.nav a[href$="#speakers"]');
  const home = document.querySelector('.nav a[data-home]');
  const sec = document.getElementById('speakers');
  if (speakers && sec && home) {
    new IntersectionObserver(([e]) => {
      speakers.classList.toggle('active', e.isIntersecting);
      home.classList.toggle('active', !e.isIntersecting);
    }, { threshold: 0.4 }).observe(sec);
  }

  // Forms (newsletter + sponsor)
  document.querySelectorAll('form[data-form]').forEach(form => {
    form.addEventListener('submit', async ev => {
      ev.preventDefault();
      const msg = form.querySelector('.form-msg');
      const data = new FormData(form);
      data.append('form', form.dataset.form);
      if (HBR.FORM_ENDPOINT) {
        try {
          const r = await fetch(HBR.FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
          if (!r.ok) throw new Error();
          form.reset();
          if (msg) msg.textContent = 'Thanks! You’re in.';
        } catch { if (msg) msg.textContent = 'Something went wrong, please try again.'; }
        return;
      }
      const lines = [...data.entries()].map(([k, v]) => `${k}: ${v}`).join('\n');
      location.href = `mailto:${HBR.CONTACT_EMAIL}?subject=${encodeURIComponent('HitBeatRun — ' + form.dataset.form)}&body=${encodeURIComponent(lines)}`;
    });
  });
})();
