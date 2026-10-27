# Fotos einbauen (Unsplash)

Aufgabe für die nächste Sitzung, ausgelöst mit „Fotos einbauen“.

Voraussetzungen (vom Kunden in den Umgebungseinstellungen eingerichtet):
- Umgebungsvariable bzw. Netzwerk-Geheimnis `UNSPLASH_ACCESS_KEY` (nur der Access Key).
- Erlaubte Domains: `api.unsplash.com`, `images.unsplash.com`.

Vorgehen:
1. Fotos über die offizielle API suchen: `GET https://api.unsplash.com/search/photos?query=…&orientation=landscape` mit Header `Authorization: Client-ID $UNSPLASH_ACCESS_KEY`.
2. Gewünschte Motive: Autos und Fuhrparks, keine Stadtansichten von Oberhausen. Ideen: Reihe von Firmenwagen/Transportern, Fahrzeug in der Werkstatt, Hand mit Autoschlüssel/Tankkarte, Transporter unterwegs, E-Fahrzeug an der Ladesäule. Keine fremden Firmenlogos auf Fahrzeugen.
3. Pro Foto den `links.download_location`-Endpunkt aufrufen (Pflicht laut Unsplash-API-Richtlinien), dann `urls.raw` mit `&w=1600&q=80&fm=jpg` herunterladen.
4. Ersetzen: `assets/img/transporter-grau.jpg` (Startbild, 5:4), `transporter-weiss.jpg` (Analyse, 4:3), `dienstwagen.jpg` (Über uns, 4:3). Gleiche Dateinamen behalten oder in `tools/build.py` anpassen.
5. Bildnachweise in `src/recht/impressum.html` und `assets/img/CREDITS.md` aktualisieren (Fotograf und „Unsplash“ mit Link; Unsplash verlangt keine Nennung, sie ist aber üblich).
6. `python3 tools/build.py`, Screenshots prüfen, committen und pushen.
