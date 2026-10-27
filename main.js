// TT Fuhrparkmanagement v4 – Navigation, Einblenden, Rechner, Formulare, Cookie-Einstellungen.

const ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Mobiles Menü
(() => {
  const kopf = document.getElementById('kopf');
  const knopf = kopf && kopf.querySelector('.menue-knopf');
  if (!knopf) return;
  const setze = (offen) => { kopf.classList.toggle('menue-offen', offen); knopf.setAttribute('aria-expanded', String(offen)); };
  knopf.addEventListener('click', () => setze(!kopf.classList.contains('menue-offen')));
  kopf.querySelectorAll('.kopf__nav a').forEach((a) => a.addEventListener('click', () => setze(false)));
  addEventListener('keydown', (e) => { if (e.key === 'Escape') setze(false); });
  const schatten = () => kopf.classList.toggle('gescrollt', scrollY > 8);
  addEventListener('scroll', schatten, { passive: true });
  schatten();
})();

// Einblenden beim Scrollen; was oberhalb der Fensterkante liegt, ist immer sichtbar.
(() => {
  const ziele = [...document.querySelectorAll('[data-auf], .schwebe')];
  const zeigen = (el) => el.classList.add('da');
  if (ruhig || !('IntersectionObserver' in window)) { ziele.forEach(zeigen); return; }
  const io = new IntersectionObserver((eintraege) => {
    for (const e of eintraege) if (e.isIntersecting) { zeigen(e.target); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
  ziele.forEach((el) => io.observe(el));
  let geplant = false;
  const nachziehen = () => { geplant = false; ziele.forEach((el) => { if (!el.classList.contains('da') && el.getBoundingClientRect().top < innerHeight) { zeigen(el); io.unobserve(el); } }); };
  addEventListener('scroll', () => { if (!geplant) { geplant = true; requestAnimationFrame(nachziehen); } }, { passive: true });
  addEventListener('load', () => setTimeout(nachziehen, 1200));
  // die schwebenden Karten im Startbild kommen kurz nach dem Foto
  document.querySelectorAll('.schwebe').forEach((el, i) => setTimeout(() => zeigen(el), 600 + i * 250));
})();

// Terminrechner: typische Intervalle je Fahrzeug bzw. Person und Jahr.
(() => {
  const fz = document.getElementById('r-fahrzeuge');
  const fa = document.getElementById('r-fahrer');
  if (!fz || !fa) return;
  const summe = document.getElementById('r-summe'), cta = document.getElementById('r-cta');
  const rechnen = () => {
    const f = Number(fz.value), p = Number(fa.value);
    document.getElementById('o-fahrzeuge').textContent = f;
    document.getElementById('o-fahrer').textContent = p;
    summe.textContent = (Math.ceil(f / 2) + f + f + f * 2 + p * 2 + 12 + 1).toLocaleString('de-DE');
    cta.textContent = `Analyse für ${f} ${f === 1 ? 'Fahrzeug' : 'Fahrzeuge'} anfragen`;
    cta.href = `index.html?fahrzeuge=${f}#kontakt`;
  };
  fz.addEventListener('input', rechnen); fa.addEventListener('input', rechnen);
  rechnen();
})();

// Fahrzeugzahl aus dem Rechner ins Formular übernehmen.
(() => {
  const anz = document.getElementById('f-anz');
  const n = new URLSearchParams(location.search).get('fahrzeuge');
  if (anz && n && /^\d{1,4}$/.test(n)) anz.value = n;
})();

// Formulare: an Netlify senden, ohne die Seite zu verlassen. Ohne Skript greift action="/danke.html".
document.querySelectorAll('form[data-senden]').forEach((form) => {
  if (!window.fetch) return;
  const hinweis = form.querySelector('[aria-live]');
  const knopf = form.querySelector('button[type="submit"]');
  const text = knopf.textContent;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    knopf.disabled = true; knopf.textContent = 'Wird gesendet …';
    try {
      const res = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      hinweis.textContent = 'Danke, Ihre Anfrage ist angekommen. Wir melden uns persönlich und zeitnah.';
      hinweis.classList.add('form-status');
      knopf.textContent = 'Gesendet';
    } catch {
      hinweis.innerHTML = 'Das hat leider nicht geklappt. Schreiben Sie uns bitte direkt an <a href="mailto:info@ttfuhrparkmanagement.com">info@ttfuhrparkmanagement.com</a>.';
      knopf.disabled = false; knopf.textContent = text;
    }
  });
});

// Cookie-Einstellungen: Auswahl im lokalen Speicher, kein Cookie. Künftige Dienste stehen als
// <script type="text/plain" data-kategorie="statistik|marketing" data-src="…"> im HTML und laden erst nach Zustimmung.
(() => {
  const SCHLUESSEL = 'tt-einwilligung';
  const banner = document.getElementById('einwilligung');
  const dialog = document.getElementById('einstellungen');
  if (!banner || !dialog) return;
  const lesen = () => { try { return JSON.parse(localStorage.getItem(SCHLUESSEL)); } catch { return null; } };
  const anwenden = (w) => {
    document.querySelectorAll('script[type="text/plain"][data-kategorie]').forEach((alt) => {
      if (!w[alt.dataset.kategorie]) return;
      const neu = document.createElement('script');
      if (alt.dataset.src) neu.src = alt.dataset.src; else neu.textContent = alt.textContent;
      alt.replaceWith(neu);
    });
    document.dispatchEvent(new CustomEvent('tt:einwilligung', { detail: w }));
  };
  const speichern = (statistik, marketing) => {
    const w = { v: 1, notwendig: true, statistik, marketing, datum: new Date().toISOString() };
    try { localStorage.setItem(SCHLUESSEL, JSON.stringify(w)); } catch { /* privater Modus */ }
    banner.hidden = true;
    anwenden(w);
  };
  const oeffnen = () => {
    const w = lesen() || {};
    dialog.querySelector('[name="statistik"]').checked = !!w.statistik;
    dialog.querySelector('[name="marketing"]').checked = !!w.marketing;
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
  };
  banner.addEventListener('click', (e) => {
    const b = e.target.closest('[data-einwilligung]');
    if (!b) return;
    if (b.dataset.einwilligung === 'alle') speichern(true, true);
    else if (b.dataset.einwilligung === 'nur-noetig') speichern(false, false);
    else oeffnen();
  });
  dialog.addEventListener('close', () => {
    if (dialog.returnValue === 'alle') speichern(true, true);
    else if (dialog.returnValue === 'auswahl') speichern(dialog.querySelector('[name="statistik"]').checked, dialog.querySelector('[name="marketing"]').checked);
  });
  document.querySelectorAll('[data-einwilligung-oeffnen]').forEach((b) => b.addEventListener('click', oeffnen));
  const gespeichert = lesen();
  if (gespeichert) anwenden(gespeichert); else banner.hidden = false;
})();
