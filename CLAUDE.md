# TT Fuhrparkmanagement – Website

Ziel: eine neue, hochwertige Website für TT Fuhrparkmanagement.

## Design
- Bei jeder Gestaltung, Überarbeitung oder Prüfung von Seiten, Sektionen, Landingpages oder App-Screens
  immer zuerst den Skill `design-taste-frontend` (`.claude/skills/taste-skill`) laden und seinem Ablauf folgen
  (Richtungen ziehen, Inspector laufen lassen, Look-and-fix-Schleife auf Screenshots).
- Arbeitsdateien des Skills liegen in `.taste-skill/` und werden nicht eingecheckt.
- Zusätzlich ist `impeccable` (`.claude/skills/impeccable`) installiert. Einsatz:
  - auf Befehl `/impeccable <befehl> <ziel>` (z. B. `audit`, `critique`, `polish`, `typeset`, `harden`),
  - für Prüfung, Barrierefreiheit, Responsiveness und Feinschliff fertiger Seiten.
- Rollenverteilung: Art Direction neuer Seiten (Richtung, Typo, Palette, Bilder) kommt aus dem taste skill;
  impeccable prüft und verfeinert. Bei widersprüchlichen Regeln gilt der taste skill.
- Außerdem sind die Skills von Emil Kowalski installiert (`.claude/skills/`, Quelle: github.com/emilkowalski/skills).
  Zuständig für Animationen und Interaktions-Details:
  - `emil-design-eng` für Details wie Schatten, Rahmen, Abstände, Zustände,
  - `animate`, `find-animation-opportunities`, `improve-animations`, `review-animations`,
    `animation-performance`, `animation-vocabulary` für Bewegung und Übergänge,
  - `break-ui` zum Stresstest der Oberfläche, `pick-ui-library` bei der Wahl von UI-Bibliotheken.
  - `mobile-native` für Smartphone-Details (Touch, Notch, 100vh, Zoom bei Eingabefeldern), `apple-design` für Gesten, Federanimationen und Typografie.
  - Nicht relevant für diese Website (nur React Native/Swift): `animate-expo`, `write-swift`.
- Reihenfolge: taste skill (Art Direction) → Emil-Skills (Bewegung, Detail) → impeccable (Prüfung, Feinschliff).

## Sprache
- Website-Texte auf Deutsch, sofern nicht anders gewünscht.
