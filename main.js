// TT Fuhrparkmanagement v2 – Bewegung und Verhalten ohne Bibliotheken.
// Regeln (nach Emil Kowalski): nur transform und opacity, ease-out für alles, was erscheint,
// nichts über 1 s, und bei reduzierter Bewegung bleibt der Inhalt, nur der Weg entfällt.

const ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fein = matchMedia('(hover: hover) and (pointer: fine)');
const clamp01 = (v) => Math.min(1, Math.max(0, v));

// Scroll-Schleife: alle scrollgebundenen Effekte in einem rAF.
const beimScrollen = [];
let geplant = false;
const lauf = () => { geplant = false; for (const f of beimScrollen) f(); };
addEventListener('scroll', () => { if (!geplant) { geplant = true; requestAnimationFrame(lauf); } }, { passive: true });
addEventListener('resize', () => requestAnimationFrame(lauf));

// Einblenden: einmal, nie dauerhaft versteckt.
(() => {
  const ziele = document.querySelectorAll('[data-auf], [data-heb]');
  document.querySelectorAll('.tabelle div').forEach((d, i) => d.style.setProperty('--r', i));
  const zeigen = (el) => el.classList.add('da');
  if (!('IntersectionObserver' in window)) { ziele.forEach(zeigen); return; }
  const io = new IntersectionObserver((eintraege) => {
    for (const e of eintraege) if (e.isIntersecting) { zeigen(e.target); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  ziele.forEach((el) => io.observe(el));
  // Sicherheitsnetz für Sprünge: alles oberhalb der Fensterunterkante ist sichtbar.
  beimScrollen.push(() => ziele.forEach((el) => { if (!el.classList.contains('da') && el.getBoundingClientRect().top < innerHeight) { zeigen(el); io.unobserve(el); } }));
  addEventListener('load', () => setTimeout(lauf, 1500));
})();

// Hero: Mitteilungen treffen nacheinander ein.
(() => {
  const m = document.querySelectorAll('.mitteilung');
  if (ruhig) { m.forEach((el) => el.classList.add('da')); return; }
  m.forEach((el, i) => setTimeout(() => el.classList.add('da'), 1100 + i * 650));
})();

// Hero: die Übersicht liegt zuerst geneigt und richtet sich beim Scrollen auf.
(() => {
  const panel = document.querySelector('.buehne__panel');
  if (!panel || ruhig) return;
  const setzen = () => {
    const r = panel.getBoundingClientRect();
    const p = clamp01(1 - (r.top - innerHeight * 0.18) / (innerHeight * 0.62));
    panel.style.transform = `rotateX(${(1 - p) * 16}deg) scale(${0.9 + p * 0.1}) translateY(${(1 - p) * 24}px)`;
  };
  beimScrollen.push(setzen);
  setzen();
})();

// Statement: Wörter füllen sich mit Farbe, während der Satz durchs Bild läuft.
(() => {
  const p = document.getElementById('fuellsatz');
  if (!p) return;
  const woerter = p.textContent.trim().split(/\s+/);
  p.setAttribute('aria-label', p.textContent.trim());
  p.innerHTML = woerter.map((w) => `<span class="wort" aria-hidden="true">${w}</span>`).join(' ');
  const spans = [...p.querySelectorAll('.wort')];
  if (ruhig) { spans.forEach((s) => s.classList.add('an')); return; }
  const setzen = () => {
    const r = p.getBoundingClientRect();
    const fortschritt = clamp01((innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.35));
    const n = Math.round(fortschritt * spans.length);
    spans.forEach((s, i) => s.classList.toggle('an', i < n));
  };
  beimScrollen.push(setzen);
  setzen();
})();

// Geschichte: Schritte rechts schalten die festgehaltene Ansicht um. Auf dem Telefon steht jede Ansicht beim Text.
(() => {
  const schritte = [...document.querySelectorAll('.schritt')];
  const ansichten = [...document.querySelectorAll('.ansicht')];
  const punkte = [...document.querySelectorAll('.punkte i')];
  if (!schritte.length) return;
  // Kopien der Ansichten für die schmale Darstellung
  schritte.forEach((s, i) => {
    const ziel = s.querySelector('.schritt__ui');
    const quelle = ansichten[i] && ansichten[i].querySelector('.ui');
    if (ziel && quelle) { ziel.appendChild(quelle.cloneNode(true)); ziel.hidden = false; }
  });
  let aktiv = 0;
  const setze = (i) => {
    if (i === aktiv) return;
    aktiv = i;
    schritte.forEach((s, k) => s.classList.toggle('an', k === i));
    ansichten.forEach((a, k) => a.classList.toggle('an', k === i));
    punkte.forEach((d, k) => d.classList.toggle('an', k === i));
  };
  beimScrollen.push(() => {
    const mitte = innerHeight * 0.5;
    let best = 0, abstand = Infinity;
    schritte.forEach((s, k) => { const r = s.getBoundingClientRect(); const d = Math.abs(r.top + r.height / 2 - mitte); if (d < abstand) { abstand = d; best = k; } });
    setze(best);
  });
})();

// Tankkarte: neigt sich leicht zum Zeiger.
(() => {
  const kachel = document.querySelector('.k-tank');
  const karte = document.querySelector('.tankkarte');
  if (!kachel || !karte || ruhig) return;
  kachel.addEventListener('pointermove', (e) => {
    if (!fein.matches) return;
    const r = kachel.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
    karte.style.setProperty('--ry', `${x * 22}deg`);
    karte.style.setProperty('--rx', `${-y * 16}deg`);
  });
  kachel.addEventListener('pointerleave', () => { karte.style.removeProperty('--ry'); karte.style.removeProperty('--rx'); });
})();

// Rechner: typische Intervalle je Fahrzeug bzw. Person und Jahr. Die Zahl rollt zum neuen Wert.
(() => {
  const fz = document.getElementById('r-fahrzeuge');
  const fa = document.getElementById('r-fahrer');
  if (!fz || !fa) return;
  const oFz = document.getElementById('o-fahrzeuge'), oFa = document.getElementById('o-fahrer');
  const summe = document.getElementById('r-summe'), cta = document.getElementById('r-cta'), anz = document.getElementById('f-anz');
  const fuellung = (el) => el.style.setProperty('--p', `${((el.value - el.min) / (el.max - el.min)) * 100}%`);
  let gezeigt = Number(summe.textContent), ziel = gezeigt, start = 0, von = gezeigt, rolle = 0;
  const rollen = (t) => {
    if (!start) start = t;
    const k = clamp01((t - start) / 420), e = 1 - Math.pow(1 - k, 3);
    gezeigt = Math.round(von + (ziel - von) * e);
    summe.textContent = gezeigt.toLocaleString('de-DE');
    if (k < 1) rolle = requestAnimationFrame(rollen);
  };
  const rechnen = () => {
    const f = Number(fz.value), p = Number(fa.value);
    oFz.textContent = f; oFa.textContent = p;
    fuellung(fz); fuellung(fa);
    const neu = Math.ceil(f / 2) + f + f + f * 2 + p * 2 + 12 + 1;
    cta.textContent = `Analyse für ${f} ${f === 1 ? 'Fahrzeug' : 'Fahrzeuge'} anfragen`;
    cta.dataset.fahrzeuge = String(f);
    if (ruhig) { summe.textContent = neu.toLocaleString('de-DE'); gezeigt = neu; return; }
    cancelAnimationFrame(rolle); von = gezeigt; ziel = neu; start = 0; rolle = requestAnimationFrame(rollen);
  };
  fz.addEventListener('input', rechnen); fa.addEventListener('input', rechnen);
  cta.addEventListener('click', () => { if (anz) { anz.value = cta.dataset.fahrzeuge || ''; anz.dispatchEvent(new Event('input')); } });
  rechnen();
})();

// Über uns: das Luftbild zoomt beim Durchscrollen langsam heraus.
(() => {
  const bild = document.querySelector('.ueber__bild img');
  if (!bild || ruhig) return;
  beimScrollen.push(() => {
    const r = bild.parentElement.getBoundingClientRect();
    const p = clamp01((innerHeight - r.top) / (innerHeight + r.height));
    bild.style.setProperty('--s', (1.14 - p * 0.14).toFixed(4));
  });
})();

// FAQ: Fragen links, die Antwort rechts. Auf dem Telefon klappt sie unter der Frage auf.
(() => {
  const knoepfe = [...document.querySelectorAll('.frage-knopf')];
  const pane = document.getElementById('antworten');
  if (!knoepfe.length || !pane) return;
  const antwort = pane.querySelector('.antwort');
  const waehle = (k, fokus) => {
    knoepfe.forEach((b) => { const an = b === k; b.setAttribute('aria-selected', String(an)); b.tabIndex = an ? 0 : -1; });
    pane.setAttribute('aria-labelledby', k.id);
    const text = k.nextElementSibling.textContent;
    if (antwort.textContent !== text) { antwort.textContent = text; antwort.classList.remove('wechsel'); void antwort.offsetWidth; antwort.classList.add('wechsel'); }
    if (fokus) k.focus();
  };
  knoepfe.forEach((k, i) => {
    k.tabIndex = i === 0 ? 0 : -1;
    k.addEventListener('click', () => waehle(k));
    k.addEventListener('pointerenter', () => { if (fein.matches) waehle(k); });
    k.addEventListener('keydown', (e) => {
      const n = e.key === 'ArrowDown' ? 1 : e.key === 'ArrowUp' ? -1 : 0;
      if (!n) return;
      e.preventDefault();
      waehle(knoepfe[(i + n + knoepfe.length) % knoepfe.length], true);
    });
  });
})();

// Kontaktformular: an Netlify senden, ohne die Seite zu verlassen. Ohne Skript greift action="/danke.html".
(() => {
  const form = document.getElementById('kontakt-form');
  if (!form || !window.fetch) return;
  const hinweis = document.getElementById('form-hinweis');
  const knopf = form.querySelector('button[type="submit"]');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    knopf.disabled = true; knopf.textContent = 'Wird gesendet …';
    try {
      const res = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      hinweis.textContent = 'Danke, Ihre Anfrage ist angekommen. Sie hören in Kürze persönlich von uns.';
      hinweis.classList.add('form-status');
      knopf.textContent = 'Anfrage gesendet';
    } catch {
      hinweis.innerHTML = 'Das hat leider nicht geklappt. Schreiben Sie uns bitte direkt an <a href="mailto:info@ttfuhrparkmanagement.com">info@ttfuhrparkmanagement.com</a>.';
      knopf.disabled = false; knopf.textContent = 'Erneut senden';
    }
  });
})();

// Footer: Uhrzeit in Oberhausen.
(() => {
  const uhr = document.getElementById('uhr');
  if (!uhr) return;
  const fmt = new Intl.DateTimeFormat('de-DE', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Berlin' });
  const stellen = () => { uhr.textContent = `${fmt.format(new Date())} Uhr`; };
  stellen(); setInterval(stellen, 30000);
})();

lauf();
