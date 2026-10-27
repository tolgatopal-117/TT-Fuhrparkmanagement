# Konzept der Website (Version 3, dunkel)

Vorgaben des Kunden: dunkles, aber nicht zu dunkles Design; kurze Startseite mit Grundinfos, Leistungen, kostenloser Analyse und Kontakt; alles Weitere auf eigenen Seiten (Reitern); modern, angelehnt an aktuelle Anbieterseiten (genannt: Avrios, Geotab); Cookie-Fenster mit Einstellungen; nicht erwähnen, dass das Unternehmen von einer Person betrieben wird.

## Richtung (taste skill)

- Gezogen: **The well-kept board** (Sektor „saas“, Ton „technical“, Markenfarben behalten). Jede Seite ist ein Brett aus Kacheln mit 8px Fugen.
- Schrift: Geist statt der gezogenen Switzer (Fontshare ist in dieser Umgebung gesperrt; Geist ist eine ähnliche Neo-Grotesk), lokal eingebunden.
- Startbild nach „Name band and rails“: Namensband, Reiterleiste, links Logo und Fakten, Mitte Fuhrpark-Übersicht und Aussage mit Schnellanfrage, rechts Farbkacheln mit der Hauptaktion.
- Aus den Vorbildern übernommen: Kurzformular direkt im ersten Bildschirm, Vertrauensreihe unter dem Startbild (mit echten Fakten statt erfundener Logos oder Bewertungen).
- Graphit (#1b1f24) statt Schwarz, helle Kacheln (#e6ebe3) als Gegengewicht, Grün nur für Aktionen.

## Seiten

| Datei | Inhalt |
| --- | --- |
| `index.html` | Startbild mit Schnellanfrage, Vertrauensreihe, acht Leistungen als Nahaufnahmen, Analyse-Reihe, Laufband, Kontakt |
| `leistungen.html` | Die acht Leistungen im Detail, Beispielansichten, Branchen |
| `so-arbeiten-wir.html` | Vier Schritte mit Akte, Preis, Terminrechner |
| `ueber-uns.html` | Wer wir sind (Wir-Form), Kontaktkarte, Werte |
| `faq.html` | Neun Fragen |
| `impressum.html`, `datenschutz.html`, `agb.html` | Rechtstexte aus `src/recht/` |

Texte ändern: in `tools/build.py` (bzw. `src/recht/*.html`) und danach `python3 tools/build.py`.

## Cookie-Einstellungen

- Die Seite setzt keine Cookies und keine Tracking-Dienste ein. Das Fenster fragt trotzdem nach, damit künftige Dienste nur mit Einwilligung geladen werden.
- Gespeichert wird die Auswahl im lokalen Speicher (`tt-einwilligung`), nicht als Cookie; Datenschutzerklärung ist angepasst.
- Künftige Dienste einbinden: `<script type="text/plain" data-kategorie="statistik" data-src="…">` – wird erst nach Zustimmung aktiv.
- „Nur notwendige“ und „Alle akzeptieren“ sind gleich gewichtet; über „Cookie-Einstellungen“ im Fuß jederzeit änderbar.

## Messung

- `lint.mjs`: 0 FAIL, 0 WARN.
- `inspect.mjs`: Start, Leistungen, So arbeiten wir, Über uns **0 FAIL** (gemessen ohne Cookie-Fenster; mit Fenster meldet der Inspector Text unter dem Fenster, weil er es nicht wegklicken kann).
- FAQ und Rechtstexte: Warnung „zu wenige Bilder“ bewusst hingenommen, es sind reine Textseiten.
- Funktionstest: Cookie-Fenster, Einstellungen speichern und wieder öffnen, alle Links, Terminrechner mit Übernahme der Fahrzeugzahl ins Formular, keine Skriptfehler.
