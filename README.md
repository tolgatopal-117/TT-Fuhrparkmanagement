# TT Fuhrparkmanagement – Website

Neue Website für TT Fuhrparkmanagement, statisches HTML/CSS/JS ohne Build-Schritt.

| Datei | Inhalt |
| --- | --- |
| `index.html` | Startseite |
| `impressum.html`, `datenschutz.html`, `agb.html` | Rechtstexte (wörtlich übernommen, ein Satz zu Schriften angepasst) |
| `danke.html` | Bestätigung nach dem Absenden des Formulars (Netlify leitet dorthin weiter), zählt die Google-Ads-Conversion, noindex |
| `404.html` | Eigene Fehlerseite (Netlify nutzt sie automatisch), noindex |
| `robots.txt`, `sitemap.xml` | Werden von `tools/build.py` erzeugt |
| `styles.css`, `main.js` | Gestaltung und Verhalten |
| `assets/` | Logo, Schrift (Hanken Grotesk, lokal), Fotos mit Nachweisen in `assets/img/CREDITS.md` |
| `docs/konzept.md` | Richtung, Idee, Aufbau, Kritik und Messwerte |

## Veröffentlichen

Netlify liest `netlify.toml`: Der Build kopiert nur die Website-Dateien nach `public/` und veröffentlicht diesen Ordner, die Skill-Ordner unter `.claude/` werden nicht mit der Website ausgeliefert.
Das Kontaktformular heißt wie bisher `kontakt` und hat dieselben Felder; Netlify Forms erkennt es über `data-netlify="true"`.

Design-Grundlage: [tasteskill](https://github.com/Leonxlnx/taste-skill) (MIT) unter `.claude/skills/taste-skill`, [impeccable](https://github.com/pbakaus/impeccable) (Apache 2.0) unter `.claude/skills/impeccable` sowie [Emil Kowalskis Skills](https://github.com/emilkowalski/skills) (MIT) unter `.claude/skills/`.

## Google-Tag und Einwilligung

- Jede Seite lädt im `<head>` zuerst die Consent-Mode-v2-Standardwerte (alles „denied“), übernimmt eine gespeicherte Auswahl und lädt dann gtag.js für `AW-18501646213` (IDs in `GTAG_IDS` in `tools/build.py`).
- `main.js` meldet Änderungen im Cookie-Fenster per `gtag('consent','update',…)` und löscht bei Widerruf die Google-Cookies.
- Conversion „Anfrage“: Snippet auf `danke.html`. Klicks auf Telefonnummern: Ereignis `phone_click` (für eine Ads-Conversion `TELEFON_CONVERSION` in `main.js` setzen).
