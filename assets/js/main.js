/* ============================================================
   HitBeatRun — site settings. Edit these three values.
   ============================================================ */
const HBR = {
  // Your Fourthwall subscription / membership page
  FOURTHWALL_URL: 'https://hitbeatrun.fourthwall.com',
  // Shown in the footer and used by the forms when no FORM_ENDPOINT is set
  CONTACT_EMAIL: 'info@hitbeatrun.com',
  // Optional: a Formspree / Getform / Basin URL so forms submit without opening email
  FORM_ENDPOINT: '',
};

(() => {
  const body = document.body;
  const root = body.dataset.root || '';
  const isLanding = body.dataset.mode === 'landing';

  // CTA wiring: on the main site "Tickets" buttons go to the subscription landing page;
  // on the landing page they go straight to Fourthwall.
  document.querySelectorAll('[data-cta]').forEach(a => {
    a.href = isLanding ? HBR.FOURTHWALL_URL : root + 'subscribe/';
    if (isLanding) { a.target = '_blank'; a.rel = 'noopener'; }
  });
  document.querySelectorAll('[data-fourthwall]').forEach(a => {
    a.href = HBR.FOURTHWALL_URL; a.target = '_blank'; a.rel = 'noopener';
  });
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

  // Reveal-on-scroll and the progress bars
  const rio = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
  }, { threshold: 0.15 });
  document.querySelectorAll('.reveal, .bars').forEach(el => rio.observe(el));

  // Course cards (+ toggles)
  document.querySelectorAll('.c-card button').forEach(b => {
    b.addEventListener('click', () => {
      const card = b.closest('.c-card');
      card.classList.toggle('open');
      b.setAttribute('aria-expanded', card.classList.contains('open'));
    });
  });

  // Sponsor carousel arrows
  const track = document.querySelector('.track');
  document.querySelector('.arrow.next')?.addEventListener('click', () => track.scrollBy({ left: 249 * 2 }));
  document.querySelector('.arrow.prev')?.addEventListener('click', () => track.scrollBy({ left: -249 * 2 }));

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
