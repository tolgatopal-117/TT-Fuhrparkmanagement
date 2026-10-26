# TT Fuhrparkmanagement – Website

Neue Website für TT Fuhrparkmanagement, statisches HTML/CSS/JS ohne Build-Schritt.

| Datei | Inhalt |
| --- | --- |
| `index.html` | Startseite |
| `impressum.html`, `datenschutz.html`, `agb.html` | Rechtstexte (wörtlich übernommen, ein Satz zu Schriften angepasst) |
| `danke.html` | Bestätigung, wenn das Formular ohne JavaScript gesendet wird |
| `styles.css`, `main.js` | Gestaltung und Verhalten |
| `assets/` | Logo, Schrift (Jost, lokal), Fotos mit Nachweisen in `assets/img/CREDITS.md` |
| `docs/konzept.md` | Richtung, Idee, Aufbau, Kritik und Messwerte |

## Veröffentlichen

Netlify liest `netlify.toml`: Der Build kopiert nur die Website-Dateien nach `public/` und veröffentlicht diesen Ordner, die Skill-Ordner unter `.claude/` werden nicht mit der Website ausgeliefert.
Das Kontaktformular heißt wie bisher `kontakt` und hat dieselben Felder; Netlify Forms erkennt es über `data-netlify="true"`.

Design-Grundlage: [tasteskill](https://github.com/Leonxlnx/taste-skill) (MIT) unter `.claude/skills/taste-skill`, [impeccable](https://github.com/pbakaus/impeccable) (Apache 2.0) unter `.claude/skills/impeccable` sowie [Emil Kowalskis Skills](https://github.com/emilkowalski/skills) (MIT) unter `.claude/skills/`.
