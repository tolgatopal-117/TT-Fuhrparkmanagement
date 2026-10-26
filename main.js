// TT Fuhrparkmanagement – kleines Skript ohne Bibliotheken. Alle Inhalte bleiben ohne JavaScript sichtbar.

// Plakette: der aktuelle Monat steht oben, wie auf einer echten HU-Plakette der Fälligkeitsmonat.
(() => {
  const ring = document.querySelector('.plakette__ring');
  if (!ring) return;
  const monat = new Date().getMonth() + 1; // 1–12; Monat m steht ohne Drehung bei -m·30°
  const ziel = (monat % 12) * 30;
  // kurze Vierteldrehung in die Endlage statt einer ganzen Runde
  ring.style.transition = 'none';
  ring.style.setProperty('--turn', `${ziel - 40}deg`);
  ring.getBoundingClientRect();
  ring.style.transition = '';
  requestAnimationFrame(() => requestAnimationFrame(() => ring.style.setProperty('--turn', `${ziel}deg`)));
})();

// Einblenden beim Scrollen, einmal und nie dauerhaft versteckt.
(() => {
  const targets = document.querySelectorAll('[data-reveal]');
  if (!targets.length) return;
  if (!('IntersectionObserver' in window)) { targets.forEach((el) => el.classList.add('is-in')); return; }
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-in');
      io.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
  targets.forEach((el) => io.observe(el));
  // Sicherheitsnetz: alles, was oberhalb der Fensterunterkante liegt, ist sichtbar, auch nach einem Sprung.
  let wartet = false;
  const nachziehen = () => {
    wartet = false;
    targets.forEach((el) => { if (!el.classList.contains('is-in') && el.getBoundingClientRect().top < innerHeight) { el.classList.add('is-in'); io.unobserve(el); } });
  };
  addEventListener('scroll', () => { if (!wartet) { wartet = true; requestAnimationFrame(nachziehen); } }, { passive: true });
  addEventListener('load', () => setTimeout(nachziehen, 2500));
})();

// Fristenrechner: typische Intervalle, je Fahrzeug bzw. je Fahrer:in und Jahr.
(() => {
  const form = document.getElementById('rechner');
  if (!form) return;
  const fz = document.getElementById('r-fahrzeuge');
  const fa = document.getElementById('r-fahrer');
  const summe = document.getElementById('r-summe');
  const monat = document.getElementById('r-monat');
  const cta = document.getElementById('r-cta');
  const anz = document.getElementById('f-anz');
  const zeile = (key) => form.parentElement.querySelector(`[data-row="${key}"]`);
  const clamp = (input) => {
    const min = Number(input.min) || 1, max = Number(input.max) || 999;
    const n = Math.round(Number(input.value));
    return Number.isFinite(n) ? Math.min(max, Math.max(min, n)) : min;
  };
  const rechnen = (pulse) => {
    const f = clamp(fz), p = clamp(fa);
    const werte = {
      hu: Math.ceil(f / 2),   // HU/AU alle 24 Monate
      uvv: f,                 // UVV-Prüfung jährlich
      wartung: f,             // Wartung meist jährlich
      reifen: f * 2,          // Sommer- und Winterreifen
      fs: p * 2,              // Führerscheinkontrolle halbjährlich
      tank: 12,               // Tankkarten-Abrechnung monatlich
      vers: 1,                // Versicherungsvergleich jährlich
    };
    let total = 0;
    for (const [k, v] of Object.entries(werte)) { total += v; const el = zeile(k); if (el) el.textContent = v.toLocaleString('de-DE'); }
    summe.textContent = total.toLocaleString('de-DE');
    const proMonat = Math.round(total / 12);
    monat.textContent = proMonat <= 1 ? 'Rund einer pro Monat. Wir behalten alle im Blick.' : `Rund ${proMonat.toLocaleString('de-DE')} pro Monat. Wir behalten alle im Blick.`;
    cta.textContent = `Analyse für ${f.toLocaleString('de-DE')} ${f === 1 ? 'Fahrzeug' : 'Fahrzeuge'} anfragen`;
    cta.dataset.fahrzeuge = String(f);
    if (pulse) { summe.classList.remove('is-pulse'); void summe.offsetWidth; summe.classList.add('is-pulse'); }
  };
  form.addEventListener('click', (e) => {
    const b = e.target.closest('[data-step]');
    if (!b) return;
    const input = document.getElementById(b.dataset.for);
    input.value = clamp(input) + Number(b.dataset.step);
    input.value = clamp(input);
    rechnen(true);
  });
  form.addEventListener('input', () => rechnen(false));
  form.addEventListener('change', (e) => { e.target.value = clamp(e.target); rechnen(true); });
  cta.addEventListener('click', () => { if (anz && cta.dataset.fahrzeuge) anz.value = cta.dataset.fahrzeuge; });
  rechnen(false);
})();

// Ablauf: ein Akkordeon, eine Stufe offen.
(() => {
  const stufen = document.querySelectorAll('.stufe');
  stufen.forEach((stufe) => {
    stufe.querySelector('.stufe__knopf').addEventListener('click', () => {
      stufen.forEach((s) => {
        const offen = s === stufe;
        s.classList.toggle('is-open', offen);
        s.querySelector('.stufe__knopf').setAttribute('aria-expanded', String(offen));
      });
    });
  });
})();

// Für wen: Index mit Vorschau, das Bild folgt der Zeile, nie dem Zeiger.
(() => {
  const root = document.querySelector('.index');
  if (!root) return;
  const frame = root.querySelector('.index__frame');
  const picture = frame.querySelector('img');
  const fine = matchMedia('(min-width: 64em)');
  const show = (row) => {
    if (!fine.matches) return;
    picture.src = row.dataset.preview;
    const y = row.offsetTop + row.offsetHeight / 2 - frame.offsetHeight / 2;
    const max = root.offsetHeight - frame.offsetHeight;
    const opening = !frame.classList.contains('is-open');
    if (opening) frame.style.transitionProperty = 'clip-path';
    frame.style.transform = `translateY(${Math.min(max, Math.max(0, y))}px)`;
    if (opening) { frame.getBoundingClientRect(); frame.style.transitionProperty = ''; }
    frame.classList.add('is-open');
  };
  root.querySelectorAll('.index__row').forEach((row) => {
    row.addEventListener('pointerenter', () => show(row));
    row.addEventListener('focus', () => show(row));
  });
})();

// Kontaktformular: an Netlify senden, ohne die Seite zu verlassen. Ohne Skript greift action="/danke.html".
(() => {
  const form = document.getElementById('kontakt-form');
  if (!form || !window.fetch) return;
  const hinweis = document.getElementById('form-hinweis');
  const knopf = form.querySelector('.senden');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    knopf.disabled = true;
    knopf.textContent = 'Wird gesendet …';
    try {
      const res = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      hinweis.textContent = 'Danke, Ihre Anfrage ist angekommen. Sie hören in Kürze persönlich von uns.';
      hinweis.classList.add('form-status');
      knopf.textContent = 'Anfrage gesendet';
    } catch {
      hinweis.innerHTML = 'Das hat leider nicht geklappt. Schreiben Sie uns bitte direkt an <a class="link" href="mailto:info@ttfuhrparkmanagement.com">info@ttfuhrparkmanagement.com</a>.';
      knopf.disabled = false;
      knopf.textContent = 'Erneut senden';
    }
  });
})();
