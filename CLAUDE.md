# TT Fuhrparkmanagement – Website

Ziel: eine neue, hochwertige Website für TT Fuhrparkmanagement.

## Design
- Vorgabe des Kunden (Oktober 2026): hell, seriös und modern wie die Fuhrpark-Anbieter Avrios und Geotab.
  Echte Fotos, Icons, weiche Karten mit leichten Schatten und dezente Verläufe sind ausdrücklich erlaubt.
  Experimentelle Layouts (Kachel-Bretter, riesige Namensbänder, Poster-Typografie) wurden abgelehnt.
- Nicht erwähnen, dass TT Fuhrparkmanagement von einer Person betrieben wird (Wir-Form). Impressum und AGB
  nennen den Inhaber, weil das gesetzlich vorgeschrieben ist.
- Keine erfundenen Kundenlogos, Bewertungen oder Kennzahlen.
- Der Skill `design-taste-frontend` (`.claude/skills/taste-skill`) dient als Werkzeugkasten: Inspector
  (`scripts/inspect.mjs`), Lint und Kritik-Ablauf nutzen; seine Stil-Verbote (Icons, Schatten, Verläufe,
  Karten-Reihen, Eyebrows) gelten für diese Website nicht. Arbeitsdateien liegen in `.taste-skill/` und
  werden nicht eingecheckt.
- Seiten werden mit `python3 tools/build.py` aus gemeinsamen Bausteinen gebaut.
- Zusätzlich ist `impeccable` (`.claude/skills/impeccable`) installiert. Einsatz:
  - auf Befehl `/impeccable <befehl> <ziel>` (z. B. `audit`, `critique`, `polish`, `typeset`, `harden`),
  - für Prüfung, Barrierefreiheit, Responsiveness und Feinschliff fertiger Seiten.
- Rollenverteilung: Die Kundenvorgabe oben bestimmt den Stil; impeccable prüft und verfeinert.
- Außerdem sind die Skills von Emil Kowalski installiert (`.claude/skills/`, Quelle: github.com/emilkowalski/skills).
  Zuständig für Animationen und Interaktions-Details:
  - `emil-design-eng` für Details wie Schatten, Rahmen, Abstände, Zustände,
  - `animate`, `find-animation-opportunities`, `improve-animations`, `review-animations`,
    `animation-performance`, `animation-vocabulary` für Bewegung und Übergänge,
  - `break-ui` zum Stresstest der Oberfläche, `pick-ui-library` bei der Wahl von UI-Bibliotheken.
  - `mobile-native` für Smartphone-Details (Touch, Notch, 100vh, Zoom bei Eingabefeldern), `apple-design` für Gesten, Federanimationen und Typografie.
  - Nicht relevant für diese Website (nur React Native/Swift): `animate-expo`, `write-swift`.
- Reihenfolge: Kundenvorgabe (Stil) → Emil-Skills (Bewegung, Detail) → impeccable (Prüfung, Feinschliff).

## Sprache
- Website-Texte auf Deutsch, sofern nicht anders gewünscht.
