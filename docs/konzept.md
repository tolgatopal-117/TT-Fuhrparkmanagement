# Konzept der neuen Website

## Richtung (taste skill)

- Gezogen: **One motif** (Seed 178455108, Sektor „other“, Markenfarben behalten).
- Neu gezogen: Hero („Tabbed folder stack“ widersprach der Komposition der Richtung, die einen riesigen, angeschnittenen Kreis verlangt; umgesetzt nach der Komposition der Richtung) und Preis („Plans that step up“ braucht drei Tarife, es gibt einen Festpreis pro Fahrzeug → „The itemised receipt“).
- Die zugeteilten Wald-Fotos wurden nicht verwendet; stattdessen echte, frei lizenzierte Fotos aus Oberhausen und der Fuhrpark-Welt.

## Idee

> Auf dieser Seite wird **die HU-Plakette** – der runde Prüfstempel mit den zwölf Monaten am Rand, den jedes Firmenfahrzeug trägt – zum **einen Motiv**: riesig und angeschnitten im Hero (mit „TT“ in der Mitte und dem aktuellen Monat oben, wie der Fälligkeitsmonat auf der echten Plakette), als Maske jedes Fotos, als Punkt vor jeder Liste, als Knopfform, als Ergebnis des Fristenrechners und als Marke im Footer.

Das lebendige Element: der **Fristenrechner**. Fahrzeuge und Fahrer:innen einstellen, die Zahl der Termine pro Jahr erscheint im Kreis, der Knopf darunter trägt die Fahrzeugzahl ins Kontaktformular.

## Aufbau (Argument)

1. Hero – was TT macht, eine Hauptaktion.
2. Statement – Plakette, Reifenwechsel, Tankabrechnung.
3. Fristenrechner – Beweis: mehr Termine, als man denkt.
4. Leistungen – acht Leistungen, ein Paket.
5. Preis – Leistungsübersicht als Beleg.
6. Ablauf – vier Schritte als Akkordeon.
7. Für wen – vier Branchen mit Vorschau.
8. Über uns – Tolga Topal, Oberhausen, keine Hotline.
9. FAQ – neun Fragen, alle aus Website, AGB und Datenschutz belegt.
10. Kontakt – Coupon mit Netlify-Formular (`name="kontakt"`, Felder wie bisher).

## Kritik, letzte Runde

```
ROUND 2
Seen in one second: Ein riesiger grüner Prüfplaketten-Kreis mit TT, daneben „Ihr Fuhrpark. Einfach erledigt.“ und ein grüner Knopf.
Idea (one sentence): Die HU-Plakette wird das eine Motiv, das die ganze Seite trägt.
Live thing: Fristenrechner (Fahrzeuge/Fahrer:innen → Termine pro Jahr, übernimmt die Fahrzeugzahl ins Formular).
Layout words by section: hero=angeschnittener Kreis / statement=Satz mit Rundbildern / fristen=Bedienung links, Zahlkreis rechts / leistungen=Kreisfoto links, Punkte rechts / preis=grünes Feld mit Beleg / ablauf=Akkordeon dunkel→hell / für wen=Index mit Vorschau / über uns=dunkles Feld mit Kreisfoto / faq=Kacheln mit stehender Überschrift / kontakt=Coupon / footer=TT aus Blöcken
Scores: design 7.5 · usability 8 · creativity 7 · content 8 → overall 7.6.
Caps applied: Kreativität auf 7 begrenzt (die Plakette passt auch zu einem Mitbewerber; TT, Oberhausen und die Bottroper Straße machen sie nur teilweise eigen).
Top three problems (most visible first):
1. Das größte Foto (Leistungen) ist eine winterliche Straße – ehrlich und vom eigenen Standort, aber das schwächste Bild. Lösung: eigenes Foto (Fahrzeug, Büro, Tolga Topal).
2. Kein bewegtes Bild; im offenen Netz fand sich kein passender, frei lizenzierter Clip.
3. Der Hero schneidet das „TT“ der Plakette am rechten Rand an; gewollt (die Richtung verlangt den Anschnitt).
```

## Messung

- `inspect.mjs`: **0 FAIL**, 2 WARN bei 1440/768/390 px.
  - `no-footage`: kein frei lizenzierter Clip gefunden.
  - `off-centre` (32 px links, 51 px rechts): Das Raster läuft von Rand zu Rand; der Messwert liest die Enden linksbündiger Zeilen.
- Vorher (alte Seite): 8 FAIL, 8 WARN.
- `lint.mjs`: 0 FAIL, 0 WARN.
- impeccable `detect`: nur statische Fehlmeldungen (Abstände werden per CSS gesetzt) und der gewollte Zickzack-Rand des Belegs.
