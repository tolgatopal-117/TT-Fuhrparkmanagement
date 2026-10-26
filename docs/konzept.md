# Konzept der Website (Version 2)

Version 1 (HU-Plakette als Motiv) wurde vom Kunden verworfen: zu schlicht, zu „KI-generiert“. Vorgabe für Version 2: Anspruch wie eine Apple-Produktseite.

## Richtung (taste skill)

- Gezogen: **The product performs** (Sektor „saas“, Ton „quiet“, Markenfarben behalten).
- Neu gesetzt, weil der Kunde ausdrücklich Apple-Niveau verlangt: Hero (das Blatt sah eine winzige 27-px-Überschrift auf zu 80 % leerer Seite vor; ersetzt durch eine große, zentrierte Überschrift mit der Fuhrpark-Übersicht als „Produkt“), Preis (eine Leistung statt Tarifvergleich), Kontakt (vollständiges Netlify-Formular statt eines einzelnen Felds).
- Bewusste Abweichungen von den Hausregeln: eine durchscheinende Navigationsleiste und iOS-artige Mitteilungen (Glas) als Teil der Apple-Anmutung. Rahmen und Schatten nur innerhalb der Oberflächen (`data-ui`).

## Idee

> Auf dieser Seite wird **das, was TT jeden Monat liefert** – Fristenübersicht, Führerscheinkontrolle, Schadenakte, Kostenreport, Tankkarte – zu **echten, arbeitenden Oberflächen**, die wie Apple-Produkte inszeniert werden.

Das lebendige Element: der **Terminrechner** (Regler für Fahrzeuge und Fahrer:innen, die Zahl rollt zum neuen Wert und wandert per Knopf ins Formular).

## Bewegung (nach Emil Kowalski)

- Hero: Überschrift steigt gestaffelt auf, drei Mitteilungen treffen nacheinander ein, die Fuhrpark-Übersicht liegt geneigt und richtet sich beim Scrollen auf.
- Statement: Wörter füllen sich beim Scrollen mit Farbe.
- „Ein Jahr Fuhrpark“: festgehaltene Bühne, vier Ansichten wechseln mit dem Text.
- Bento: Tankkarte neigt sich zum Zeiger; Balken wachsen.
- Rechner: Zahl rollt; Ablauf: Fortschrittsbalken der Akte füllen sich; Luftbild zoomt beim Scrollen.
- Nur `transform` und `opacity`, ease-out, maximal 0,9 s; bei reduzierter Bewegung bleibt alles sichtbar.
- Ab dem Preis gleiten Inhalte nur in Position und sind nie unsichtbar (lange Seite, nichts soll versteckt bleiben).

## Kritik, letzte Runde

```
ROUND 3
Seen in one second: „Ihr Fuhrpark. Einfach erledigt.“ groß und zentriert, darunter eine Fuhrpark-Übersicht mit eintreffenden Mitteilungen.
Idea (one sentence): TTs Leistungen erscheinen als echte, arbeitende Oberflächen, inszeniert wie Apple-Produkte.
Live thing: Terminrechner mit Reglern.
Layout words by section: hero=zentriert + Produkt / statement=Füllsatz / story=festgehaltene Bühne / leistungen=Bento / rechner=schwarzes Feld mit Riesenzahl / preis=große Liste / ablauf=vier Farbfelder mit Akte / über uns=Luftbild + Brief / faq=Fragen links, Antwort rechts / kontakt=Formular auf Karte / footer=Kacheln
Scores: design 8 · usability 8.5 · creativity 7.5 · content 8 → overall 8.0.
Caps applied: keine harte Kappung; die Fotoqualität begrenzt den Eindruck (nur drei echte Fotos).
Top three problems:
1. Zu wenige und zu schwache Fotos. Lösung: eigene Fotos (Porträt, Fahrzeuge, Büro) oder Unsplash über API-Schlüssel.
2. Kein bewegtes Bild (Video).
3. Die Akte im Ablauf und die Bento-Kacheln sind auf dem Tablet sehr ähnlich (Warnung „card-rows“).
```

## Messung

- `inspect.mjs`: **0 FAIL**, 6 WARN (Glas, Schriftgrößen inkl. Oberflächen, wenige Fotos, kein Video, Randmessung, ähnliche Kacheln auf dem Tablet).
- `lint.mjs`: 0 FAIL, 0 WARN.
- impeccable `detect`: verbleibend nur der gewollte Grauton des Füllsatzes und statische Fehlmeldungen zu Abständen.
- Funktionstest: Rechner, Formular-Übernahme, FAQ per Maus und Tastatur, Geschichte, Rechtsseiten, ohne JavaScript und bei reduzierter Bewegung alles sichtbar.
