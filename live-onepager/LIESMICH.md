# Live-Seite (Einseiter) – Upload-Ordner für Netlify

Dieser Ordner ist die Website, wie sie auf ttfuhrparkmanagement.com läuft: Design unverändert, Inhalte ergänzt (November 2026).
Er wird **per Hand** bei Netlify hochgeladen: Projekt öffnen → Deploys → den ganzen Ordner (ohne diese Datei, schadet aber auch nicht) in das Upload-Feld ziehen.

| Datei | Inhalt |
| --- | --- |
| `index.html` | Startseite inkl. Google-Tag mit Consent Mode v2, Cookie-Hinweis, FAQ, Impressum, Datenschutz, AGB (als Fenster) |
| `danke.html` | Bestätigung nach dem Absenden des Formulars, enthält das Google-Ads-Conversion-Snippet, noindex |
| `404.html` | Fehlerseite, noindex |
| `logo-tt.png` | Logo (vorher in die Seite eingebettet) |
| `robots.txt`, `sitemap.xml`, Icons | Technik |

Hinweise:
- Das Formular braucht `data-netlify='true'` im HTML. Netlify entfernt das Attribut beim Ausliefern; wer die Live-Seite herunterlädt und wieder hochlädt, muss es also wieder einsetzen.
- `danke.html` und `404.html` übernehmen Kopf, Fuß und Rechtstexte aus `index.html`. Bei Änderungen an Rechtstexten alle drei Dateien anpassen.
- Datenschutz-Ergänzungen sind im Quelltext mit „von Claude ergänzt – rechtlich prüfen lassen“ markiert.
- Anruf-Klicks senden das Ereignis `phone_click`. Für eine Google-Ads-Conversion `TELEFON_CONVERSION` in `index.html` setzen.
