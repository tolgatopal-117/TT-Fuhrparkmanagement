"""Baut alle Seiten der Website (Version 4) aus gemeinsamen Bausteinen.

Aufruf aus dem Projektordner:  python3 tools/build.py
Texte hier ändern (Rechtstexte in src/recht/*.html) und danach neu bauen.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SITE = "https://ttfuhrparkmanagement.com"
TELEFON = "+49 156 30158503"
TEL_LINK = "tel:+4915630158503"
MAIL = "info@ttfuhrparkmanagement.com"
FLOTTERO = "https://flottero.de"

# Google-Tag (Google Ads). Weitere IDs (z. B. ein späteres GA4 „G-…“) hier ergänzen:
# gtag.js wird nur einmal geladen, jede ID bekommt ihr eigenes gtag('config', …).
GTAG_IDS = ["AW-18501646213"]

# Conversion „Anfrage gesendet“, nur auf danke.html (Snippet aus Google Ads, unverändert)
CONVERSION = """  <script>
    gtag('event', 'conversion', {
        'send_to': 'AW-18501646213/328CCKjTnLodEIXvovZE',
        'value': 1.0,
        'currency': 'EUR'
    });
  </script>
"""

NAV = [
    ("leistungen.html", "Leistungen"),
    ("so-arbeiten-wir.html", "So arbeiten wir"),
    ("ueber-uns.html", "Über uns"),
    ("faq.html", "FAQ"),
    ("index.html#kontakt", "Kontakt"),
]

# Sichtbarer Platzhalter für Inhalte, die der Inhaber noch liefern muss
def todo(text):
    return f'<mark class="todo">TODO: {text}</mark>'

# Symbole nach Lucide (ISC-Lizenz), als Pfade eines 24er-Rasters
ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "pfeil": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "runter": '<path d="m6 9 6 6 6-6"/>',
    "ausweis": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M15 8h2"/><path d="M15 12h2"/><path d="M7 16h10"/>',
    "kalender": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    "ordner": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "werkzeug": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "auto": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    "schild": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "tank": '<path d="M3 22h12"/><path d="M4 9h10"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2a2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L18 5"/>',
    "diagramm": '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "telefon": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "ort": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "person": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "euro": '<path d="M4 10h12"/><path d="M4 14h9"/><path d="M19 6a7.7 7.7 0 0 0-5.2-2A7.9 7.9 0 0 0 6 12c0 4.4 3.5 8 7.8 8 2 0 3.8-.8 5.2-2"/>',
    "schloss": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "auszeichnung": '<path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>',
    "lupe": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "dokument": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
    "kreislauf": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "glocke": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "lkw": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "hammer": '<path d="m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>',
    "koffer": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "gebaeude": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    "schluessel": '<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r=".5" fill="currentColor"/>',
    "herz": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "helm": '<path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M14 6a6 6 0 0 1 6 6v3"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><rect x="2" y="15" width="20" height="4" rx="1"/>',
    "monitor": '<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
    "extern": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def icon_box(name):
    return f'<span class="icon">{icon(name)}</span>'


LEISTUNGEN = [
    ("fuehrerschein", "ausweis", "Führerscheinkontrolle", "Regelmäßige, dokumentierte Prüfung der Fahrerlaubnis aller Fahrer:innen zur Absicherung der Halterhaftung.",
     ["Prüfung in festen Abständen", "Dokumentation jeder Kontrolle", "Erinnerung bei fälligen Kontrollen"]),
    ("termine", "kalender", "Terminüberwachung", "Erinnerung an gesetzliche und technische Fristen, damit kein Termin verstreicht.",
     ["HU und AU", "UVV-Prüfung", "Wartung und Reifenwechsel"]),
    ("dokumente", "ordner", "Dokumentenverwaltung", "Digitale Ablage aller Unterlagen, getrennt je Kunde und jederzeit auffindbar.",
     ["Fahrzeugscheine", "Versicherungspolicen", "Leasing- und Kaufverträge"]),
    ("werkstatt", "werkzeug", "Werkstattkoordination", "Wir kümmern uns um Werkstatttermine und behalten die Kosten im Griff.",
     ["Termine vereinbaren", "Angebote einholen", "Rechnungen auf Plausibilität prüfen"]),
    ("schaden", "auto", "Schadenmanagement", "Vom ersten Foto bis zum abgeschlossenen Fall, ohne dass Sie hinterhertelefonieren müssen.",
     ["Aufnahme und Dokumentation", "Meldung an Versicherung und Werkstatt", "Nachverfolgung bis zum Abschluss"]),
    ("versicherung", "schild", "Versicherungsmanagement", "Wir behalten die Fristen Ihrer bestehenden Versicherungsverträge im Blick und übernehmen im Schadenfall die Kommunikation mit dem Versicherer.",
     ["Überwachung von Fristen und Laufzeiten", "Kommunikation mit dem Versicherer im Schadenfall", "Unterlagen griffbereit"]),
    ("tankkarten", "tank", "Tankkartenverwaltung", "Jede Tankkarte ist einem Fahrzeug und einer Person zugeordnet.",
     ["Zuordnung zu Fahrzeugen und Fahrer:innen", "Prüfung der Monatsabrechnung", "Auffälligkeiten klären"]),
    ("kosten", "diagramm", "Kosten-Reporting", "Sie sehen jederzeit, was Ihr Fuhrpark kostet und wo das Geld hinfährt.",
     ["Kosten je Fahrzeug", "Kosten pro Kilometer", "Regelmäßige Aufstellung"]),
    ("beschaffung", "schluessel", "Firmenwagen-Beschaffung", "Sie brauchen ein neues Fahrzeug? Wir holen in Ihrem Auftrag Angebote ein, für Kauf oder Leasing, und stellen sie übersichtlich gegenüber. Die Entscheidung treffen Sie.",
     ["Angebote einholen, Kauf oder Leasing", "Übersichtlicher Vergleich", "Die Entscheidung bleibt bei Ihnen"]),
]

SCHRITTE = [
    ("Erstgespräch", "Sie rufen an oder schreiben uns. Im kurzen Gespräch klären wir, wie Ihr Fuhrpark aufgestellt ist und wo es im Alltag hakt."),
    ("Fuhrpark-Check", "Wir sichten kostenlos Fahrzeuge, Fristen, Verträge und Unterlagen und zeigen Ihnen, was wir übernehmen können. Danach erhalten Sie Ihr Angebot."),
    ("Laufende Betreuung", "Wir digitalisieren Ihre Unterlagen und übernehmen die Verwaltung: Fristen, Werkstatt, Schäden und Kosten-Reporting, mit festem Ansprechpartner."),
]

BRANCHEN = [
    ("hammer", "Handwerk", "Transporter, die nicht ausfallen dürfen: Werkstatttermine, HU und UVV-Prüfung rechtzeitig geregelt."),
    ("herz", "Pflegedienste", "Viele Fahrzeuge, wechselnde Fahrer:innen: Führerscheinkontrolle und Schäden sauber dokumentiert."),
    ("helm", "Bau", "Fahrzeuge im harten Einsatz: Schäden, Werkstatt und Fristen, ohne dass die Baustelle wartet."),
    ("koffer", "Weitere Betriebe", "Außendienst, Service oder Verwaltung: Dieselben Pflichten, auch bei wenigen Fahrzeugen."),
]

# (Frage, Antwort, auf der Startseite zeigen)
FRAGEN = [
    ("Was kostet das?", "Sie zahlen einen festen Preis pro Fahrzeug, alle neun Leistungsbausteine sind enthalten. Ihr genaues Angebot erhalten Sie nach dem Fuhrpark-Check. Der Check selbst ist kostenlos und unverbindlich.", True),
    ("Bin ich an einen Versicherer gebunden?", "Nein. Sie behalten Ihre bestehenden Versicherungsverträge und entscheiden selbst, bei wem Sie versichert sind. Wir vermitteln keine Versicherungen. Wir überwachen die Fristen Ihrer Verträge und übernehmen im Schadenfall die Kommunikation mit dem Versicherer.", True),
    ("Holen Sie auch Angebote für neue Firmenwagen ein?", "Ja. Wenn Sie ein Fahrzeug brauchen, holen wir in Ihrem Auftrag Angebote ein, für Kauf oder Leasing, und stellen sie übersichtlich nebeneinander. Ob und wo Sie abschließen, entscheiden Sie selbst. Fahrzeuge oder Leasingverträge vermitteln wir nicht.", True),
    ("Wie schnell geht der Start?", f"Auf Ihre Anfrage melden wir uns innerhalb eines Werktags und vereinbaren das Erstgespräch. Danach folgt der kostenlose Fuhrpark-Check. Die Übergabe kann sehr kurzfristig stattfinden: Sobald Fahrzeugscheine, Policen und Verträge vorliegen, übernehmen wir die laufende Betreuung.", True),
    ("Arbeiten Sie auch außerhalb von Duisburg?", "Ja. Wir betreuen Betriebe in Duisburg und im Umkreis von rund 70 Kilometern, also im Ruhrgebiet und am Niederrhein. Vieles läuft ohnehin per Telefon und E-Mail.", True),
    ("Welche Leistungen sind im Paket enthalten?", "Alle neun: Führerscheinkontrolle, Terminüberwachung, Dokumentenverwaltung, Werkstattkoordination, Schadenmanagement, Versicherungsmanagement, Tankkartenverwaltung, Kosten-Reporting und die Beschaffung von Firmenwagen-Angeboten. Sie erhalten immer das komplette Paket.", False),
    ("Lohnt sich das auch für wenige Fahrzeuge?", "Ja. Auch bei wenigen Fahrzeugen fallen Fristen, Führerscheinkontrollen, Schäden und Unterlagen an. Wir nehmen Ihnen diese Arbeit ab, unabhängig von der Größe Ihres Fuhrparks.", False),
    ("Bleibe ich Halter meiner Fahrzeuge?", "Ja. Die Halter- und Unternehmerpflichten bleiben bei Ihnen. Wir übernehmen die organisatorischen und koordinierenden Aufgaben und sorgen dafür, dass nichts liegen bleibt.", False),
    ("Wie lange läuft der Vertrag?", "Laufzeit und Kündigungsfristen stehen in Ihrem Rahmenvertrag. Ist nichts anderes vereinbart, können Sie mit einer Frist von einem Monat zum Monatsende kündigen.", False),
    ("Was passiert mit den Daten meiner Fahrer?", "Wir verarbeiten sie als Auftragsverarbeiter nach Art. 28 DSGVO, nur nach Ihrer Weisung und auf Grundlage eines Auftragsverarbeitungsvertrags. Nach Vertragsende geben wir die Daten zurück oder löschen sie innerhalb von 30 Tagen, sofern keine Aufbewahrungspflicht besteht.", False),
]


def bild(name, alt, w, h, lazy=True, sizes="(max-width: 64em) 100vw, 50vw"):
    """Foto als <picture>: WebP in zwei Breiten, JPEG als Rückfall."""
    laden = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    return (f'<picture><source type="image/webp" srcset="/assets/img/{name}-768.webp 768w, /assets/img/{name}-1280.webp 1280w" sizes="{sizes}">'
            f'<img src="/assets/img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {laden}></picture>')


def faq_liste(fragen):
    return "\n".join(f'    <details class="frage"{" open" if i == 0 else ""} data-auf><summary>{q}{icon("runter")}</summary><p>{a}</p></details>' for i, (q, a, _) in enumerate(fragen))


# ---------------------------------------------------------------- Rahmen
def google_tag():
    """Consent Mode v2: erst alles auf „denied“, dann eine gespeicherte Einwilligung übernehmen, dann gtag.js laden.
    Ohne Einwilligung setzt Google keine Cookies (nur cookielose Pings). Schlüssel und Felder wie in main.js."""
    configs = "".join(f"gtag('config','{i}');" for i in GTAG_IDS)
    return f"""  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('consent', 'default', {{ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied', wait_for_update: 500}});
    gtag('set', 'ads_data_redaction', true);
    try {{
      var w = JSON.parse(localStorage.getItem('tt-einwilligung'));
      if (w) gtag('consent', 'update', {{
        ad_storage: w.marketing ? 'granted' : 'denied', ad_user_data: w.marketing ? 'granted' : 'denied',
        ad_personalization: w.marketing ? 'granted' : 'denied', analytics_storage: w.statistik ? 'granted' : 'denied'
      }});
    }} catch (e) {{}}
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_IDS[0]}"></script>
  <script>gtag('js', new Date());{configs}</script>
"""


def strukturierte_daten():
    """Nur Angaben, die auch im Impressum stehen; areaServed laut Vorgabe des Inhabers."""
    daten = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "TT Fuhrparkmanagement",
        "url": SITE + "/",
        "logo": SITE + "/assets/logo-tt.png",
        "image": SITE + "/assets/img/transporter-grau.jpg",
        "telephone": TELEFON,
        "address": {"@type": "PostalAddress", "streetAddress": "Bottroper Str. 87", "postalCode": "46117", "addressLocality": "Oberhausen", "addressCountry": "DE"},
        "areaServed": [{"@type": "City", "name": "Duisburg"}, {"@type": "Place", "name": "Ruhrgebiet"}, {"@type": "Place", "name": "Niederrhein"}],
        "description": BESCHREIBUNG,
    }
    return f'  <script type="application/ld+json">{json.dumps(daten, ensure_ascii=False)}</script>\n'


def kopf(titel, beschreibung, aktiv, robots=False, pfad=None, extra=""):
    meta_robots = '\n  <meta name="robots" content="noindex">' if robots else ""
    url = SITE + "/" + ("" if pfad == "index.html" else pfad) if pfad else None
    seo = ""
    if url:
        seo = f"""
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="TT Fuhrparkmanagement">
  <meta property="og:title" content="{titel}">
  <meta property="og:description" content="{beschreibung}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/transporter-grau.jpg">
  <meta property="og:image:width" content="1280">
  <meta property="og:image:height" content="750">
  <meta name="twitter:card" content="summary_large_image">"""
    links = []
    for href, name in NAV:
        cur = ' aria-current="page"' if href == aktiv else ""
        links.append(f'<a href="{href}"{cur}>{name}</a>')
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
{google_tag()}{extra}  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titel}</title>
  <meta name="description" content="{beschreibung}">{meta_robots}{seo}
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" href="/favicon-48x48.png" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="styles.css">
  <script>document.documentElement.classList.add('js')</script>
{strukturierte_daten() if pfad == "index.html" else ""}</head>
<body>
<header class="kopf" id="kopf">
  <div class="container kopf__innen">
    <a class="kopf__logo" href="index.html" aria-label="TT Fuhrparkmanagement, zur Startseite"><img src="assets/logo-tt.png" alt="TT Fuhrparkmanagement" width="600" height="167"></a>
    <button class="menue-knopf" type="button" aria-expanded="false" aria-controls="hauptnav" aria-label="Menü"><span></span></button>
    <nav class="kopf__nav" id="hauptnav" aria-label="Hauptnavigation">
      {''.join(links)}
      <a class="btn btn--primary" href="index.html#kontakt">Fuhrpark-Check anfragen</a>
    </nav>
  </div>
</header>
"""


def fuss():
    return f"""<footer class="fuss">
  <div class="container">
    <div class="fuss__raster">
      <div>
        <h2 class="sr-only">TT Fuhrparkmanagement</h2>
        <p style="margin-top:0;color:#fff;font-weight:600;font-size:1.0625rem">TT Fuhrparkmanagement</p>
        <p>Wir übernehmen die Verwaltung Ihrer Firmenfahrzeuge. Zum festen Preis pro Fahrzeug, mit festem Ansprechpartner.</p>
      </div>
      <div>
        <h2>Unternehmen</h2>
        <ul>
          <li><a href="leistungen.html">Leistungen</a></li>
          <li><a href="so-arbeiten-wir.html">So arbeiten wir</a></li>
          <li><a href="ueber-uns.html">Über uns</a></li>
          <li><a href="faq.html">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h2>Rechtliches</h2>
        <ul>
          <li><a href="impressum.html">Impressum</a></li>
          <li><a href="datenschutz.html">Datenschutz</a></li>
          <li><a href="agb.html">AGB</a></li>
          <li><button type="button" class="fuss__knopf" data-einwilligung-oeffnen>Cookie-Einstellungen</button></li>
        </ul>
      </div>
      <div>
        <h2>Kontakt</h2>
        <ul>
          <li><a href="{TEL_LINK}">{TELEFON}</a></li>
          <li><a href="mailto:{MAIL}">{MAIL}</a></li>
          <li>Bottroper Str. 87<br>46117 Oberhausen</li>
        </ul>
      </div>
    </div>
    <div class="fuss__zeile"><span>© 2026 TT Fuhrparkmanagement</span><span>Ihr Fuhrpark, unser Antrieb.</span></div>
  </div>
</footer>
<nav class="mobil-leiste" aria-label="Schnellkontakt">
  <a class="btn btn--ghost" href="{TEL_LINK}">{icon('telefon')} Anrufen</a>
  <a class="btn btn--primary" href="index.html#kontakt">Anfragen</a>
</nav>
<div class="einwilligung" id="einwilligung" role="region" aria-label="Cookie-Einstellungen" hidden>
  <h2>Ihre Privatsphäre</h2>
  <p>Mit Ihrer Einwilligung setzen wir Cookies von Google Ads ein, um zu messen, ob eine Anfrage über unsere Anzeigen zustande kam. Ohne Einwilligung werden keine Werbe- oder Analyse-Cookies gesetzt. Sie können Ihre Wahl jederzeit unter „Cookie-Einstellungen“ ändern. Mehr in der <a href="datenschutz.html#cookies">Datenschutzerklärung</a>.</p>
  <div class="einwilligung__knoepfe">
    <button type="button" class="btn btn--wahl" data-einwilligung="nur-noetig">Nur notwendige</button>
    <button type="button" class="btn btn--wahl" data-einwilligung="alle">Alle akzeptieren</button>
    <button type="button" class="einwilligung__link" data-einwilligung="einstellungen">Einstellungen</button>
  </div>
</div>
<dialog class="einstellungen" id="einstellungen" aria-labelledby="einstellungen-titel">
  <form method="dialog" class="einstellungen__form">
    <h2 id="einstellungen-titel">Cookie-Einstellungen</h2>
    <p>Wählen Sie, welche Dienste wir verwenden dürfen. Sie können Ihre Auswahl jederzeit über „Cookie-Einstellungen“ im Fußbereich ändern oder widerrufen.</p>
    <div class="kategorie"><div><b>Notwendig</b><p>Speichert Ihre Auswahl im lokalen Speicher Ihres Browsers. Immer aktiv.</p></div><input type="checkbox" class="schalter-feld" checked disabled aria-label="Notwendig, immer aktiv"></div>
    <div class="kategorie"><div><b>Statistik</b><p>Auswertung, wie die Website genutzt wird. Derzeit nicht im Einsatz.</p></div><input type="checkbox" class="schalter-feld" name="statistik" aria-label="Statistik erlauben"></div>
    <div class="kategorie"><div><b>Marketing</b><p>Google Ads Conversion-Tracking (Google Ireland Ltd.): misst, ob eine Anfrage oder ein Anruf über eine Anzeige zustande kam. Setzt Cookies.</p></div><input type="checkbox" class="schalter-feld" name="marketing" aria-label="Marketing erlauben"></div>
    <div class="einwilligung__knoepfe">
      <button type="submit" class="btn btn--wahl" value="auswahl">Auswahl speichern</button>
      <button type="submit" class="btn btn--wahl" value="alle">Alle akzeptieren</button>
    </div>
  </form>
</dialog>
<script src="main.js" defer></script>
</body>
</html>
"""


def aufruf():
    return f"""<section class="section" aria-labelledby="aufruf-titel">
  <div class="container">
    <div class="aufruf" data-auf>
      <div>
        <h2 id="aufruf-titel">Mehr Zeit fürs Kerngeschäft?</h2>
        <p>Im kostenlosen Fuhrpark-Check zeigen wir Ihnen, was wir Ihnen abnehmen können. Unverbindlich.</p>
      </div>
      <div class="aufruf__knoepfe">
        <a class="btn btn--primary" href="index.html#kontakt">Kostenlosen Fuhrpark-Check anfragen {icon('pfeil')}</a>
        <a class="btn btn--ghost" href="{TEL_LINK}">{icon('telefon')} {TELEFON}</a>
      </div>
    </div>
  </div>
</section>
"""


def seitenkopf(titel, text, krume):
    return f"""<section class="seitenkopf">
  <div class="container">
    <p class="krumen"><a href="index.html">Start</a> / {krume}</p>
    <h1>{titel}</h1>
    {f'<p class="lead">{text}</p>' if text else ''}
  </div>
</section>
"""


# ---------------------------------------------------------------- Startseite
def startseite():
    karten = "\n".join(
        f'      <a class="karte" href="leistungen.html#{a}" data-auf style="--i:{i % 4}">{icon_box(ic)}<h3>{n}</h3><p>{t}</p><span class="link">Mehr erfahren {icon("pfeil")}</span></a>'
        for i, (a, ic, n, t, _) in enumerate(LEISTUNGEN))
    schritte = "\n".join(
        f'      <li class="schritt" data-auf style="--i:{i}"><span class="schritt__nr">{i + 1}</span><h3>{n}</h3><p>{t}</p></li>'
        for i, (n, t) in enumerate(SCHRITTE))
    branchen = "\n".join(f'      <div class="karte" data-auf style="--i:{i}">{icon_box(ic)}<h3>{n}</h3><p>{t}</p></div>' for i, (ic, n, t) in enumerate(BRANCHEN))
    fragen = faq_liste([f for f in FRAGEN if f[2]])
    return f"""<main id="top">
<section class="hero">
  <div class="container hero__raster">
    <div>
      <p class="marke" data-auf>Externes Fuhrparkmanagement für Duisburg, Ruhrgebiet und Niederrhein</p>
      <h1 data-auf style="--i:1">Wir übernehmen die Fuhrpark&shy;verwaltung für Ihren Betrieb.</h1>
      <p class="lead" data-auf style="--i:2">Für Handwerk, Pflegedienste und Bau mit 5 bis 50 Fahrzeugen: Führerscheinkontrolle, Fristen, Werkstatt, Schäden und Kosten in einer Hand, mit festem Ansprechpartner. So bleibt Ihnen mehr Zeit fürs Kerngeschäft.</p>
      <div class="hero__aktionen" data-auf style="--i:3">
        <a class="btn btn--primary" href="#kontakt">Kostenlosen Fuhrpark-Check anfragen {icon('pfeil')}</a>
        <a class="btn btn--ghost" href="{TEL_LINK}">{icon('telefon')} {TELEFON}</a>
      </div>
      <ul class="haken-liste" data-auf style="--i:4">
        <li>{icon('check')} Kostenloser Fuhrpark-Check</li>
        <li>{icon('check')} Fester Ansprechpartner</li>
        <li>{icon('check')} Mehr Zeit fürs Kerngeschäft</li>
      </ul>
    </div>
    <div class="hero__bild" data-auf style="--i:2">
      <div class="hero__foto">{bild('transporter-grau', 'Grauer Transporter auf einem Parkplatz', 1280, 750, lazy=False)}</div>
      <div class="schwebe schwebe--2"><span class="schwebe__icon">{icon('glocke')}</span><div><b>Fristen im Blick</b><span>HU, AU und UVV rechtzeitig vereinbart</span></div></div>
      <div class="schwebe schwebe--1"><span class="schwebe__icon">{icon('person')}</span><div><b>Fester Ansprechpartner</b><span>Persönlich statt Hotline</span></div></div>
    </div>
  </div>
</section>

<section aria-label="Worauf Sie sich verlassen können">
  <div class="container">
    <ul class="fakten">
      <li class="fakt" data-auf>{icon_box('euro')}<div><b>Fester Preis pro Fahrzeug</b><span>Ohne Einzelbuchung, ohne Aufpreis</span></div></li>
      <li class="fakt" data-auf style="--i:1">{icon_box('person')}<div><b>Fester Ansprechpartner</b><span>Kein Callcenter, kein Ticketsystem</span></div></li>
      <li class="fakt" data-auf style="--i:2">{icon_box('schloss')}<div><b>Datenschutz nach DSGVO</b><span>Mit Auftragsverarbeitungsvertrag</span></div></li>
      <li class="fakt" data-auf style="--i:3">{icon_box('auszeichnung')}<div><b>Zertifizierte Verwaltung</b><span>Fachwissen zu Halterhaftung und Prüfpflichten</span></div></li>
    </ul>
  </div>
</section>

<section class="section" id="fuer-wen" aria-labelledby="fuer-wen-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf>
      <p class="marke">Für wen</p>
      <h2 id="fuer-wen-titel">Für Betriebe mit 5 bis 50 Fahrzeugen</h2>
      <p class="lead">Zu groß, um den Fuhrpark nebenbei zu verwalten, zu klein für eine eigene Fuhrparkabteilung.</p>
    </div>
    <div class="karten">
{branchen}
    </div>
  </div>
</section>

<section class="section section--soft" id="leistungen" aria-labelledby="leistungen-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf>
      <p class="marke">Leistungen</p>
      <h2 id="leistungen-titel">Neun Bausteine. Ein Paket.</h2>
      <p class="lead">Alle Bausteine sind immer enthalten. Sie geben die Arbeit ab, wir kümmern uns.</p>
    </div>
    <div class="karten karten--drei">
{karten}
    </div>
  </div>
</section>

<section class="section" id="ablauf" aria-labelledby="start-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf>
      <p class="marke">Ablauf</p>
      <h2 id="start-titel">In drei Schritten zur externen Fuhrparkverwaltung</h2>
    </div>
    <ol class="schritte">
{schritte}
    </ol>
  </div>
</section>

<section class="section section--soft" id="check" aria-labelledby="analyse-titel">
  <div class="container teilung">
    <div class="teilung__bild" data-auf>{bild('transporter-weiss', 'Weißer Transporter von hinten auf einem Parkplatz', 1280, 720)}</div>
    <div data-auf style="--i:1">
      <p class="marke">Kostenlos und unverbindlich</p>
      <h2 id="analyse-titel">Der kostenlose Fuhrpark-Check</h2>
      <p class="lead">Bevor Sie sich entscheiden, schauen wir uns Ihren Fuhrpark an und zeigen Ihnen, wo Sie Aufwand sparen.</p>
      <ul class="punkte">
        <li>{icon_box('lupe')}<div><b>Bestand und Fristen sichten</b><span>Welche Fahrzeuge, welche Termine stehen an?</span></div></li>
        <li>{icon_box('dokument')}<div><b>Verträge und Unterlagen sichten</b><span>Leasing, Versicherungen, Tankkarten</span></div></li>
        <li>{icon_box('euro')}<div><b>Ihr Angebot zum Festpreis</b><span>Ein Preis pro Fahrzeug, alles inklusive</span></div></li>
      </ul>
      <a class="btn btn--primary" href="#kontakt">Kostenlosen Fuhrpark-Check anfragen {icon('pfeil')}</a>
    </div>
  </div>
</section>

<section class="section" id="flottero" aria-label="Unser Werkzeug: Flottero" style="padding-block:clamp(2.5rem, 5vw, 4rem)">
  <div class="container">
    <div class="werkzeug" data-auf style="margin-top:0">
      {icon_box('monitor')}
      <div>
        <h3>Unser Werkzeug: Flottero</h3>
        <p>Für die Verwaltung setzen wir unsere eigene Fuhrparksoftware Flottero ein. Darin laufen Fahrzeuge, Fristen, Dokumente und Kosten Ihres Fuhrparks an einer Stelle zusammen.</p>
      </div>
      <a class="btn btn--ghost" href="{FLOTTERO}" target="_blank" rel="noopener">flottero.de {icon('extern')}</a>
    </div>
  </div>
</section>

<section class="section section--soft" id="fragen" aria-labelledby="fragen-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf>
      <p class="marke">FAQ</p>
      <h2 id="fragen-titel">Häufige Fragen</h2>
    </div>
    <div class="faq">
{fragen}
      <a class="link" href="faq.html" style="justify-self:center;margin-top:.75rem">Alle Fragen ansehen {icon('pfeil')}</a>
    </div>
  </div>
</section>

<section class="section" id="kontakt" aria-labelledby="kontakt-titel">
  <div class="container kontakt__raster">
    <div data-auf>
      <p class="marke">Kontakt</p>
      <h2 id="kontakt-titel">Kostenlosen Fuhrpark-Check anfragen</h2>
      <p class="lead" style="margin-top:1rem">Erzählen Sie uns kurz von Ihrem Fuhrpark. Wir melden uns innerhalb eines Werktags. Fuhrpark-Check und Erstgespräch sind kostenlos und unverbindlich.</p>
      <div class="kontakt__daten">
        <a href="{TEL_LINK}">{icon_box('telefon')}<span><small>Telefon</small><b>{TELEFON}</b></span></a>
        <a href="mailto:{MAIL}">{icon_box('mail')}<span><small>E-Mail</small><b>{MAIL}</b></span></a>
        <div>{icon_box('ort')}<span><small>Adresse</small><b>Bottroper Str. 87, 46117 Oberhausen</b></span></div>
      </div>
    </div>
    <form class="formular" name="kontakt" id="kontakt-form" method="POST" action="/danke.html" data-netlify="true" netlify-honeypot="bot-field" data-senden data-auf style="--i:1">
      <h3>Ihre Anfrage</h3>
      <input type="hidden" name="form-name" value="kontakt">
      <p class="hp"><label>Bitte nicht ausfüllen: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="zwei">
        <div class="feld"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="feld"><label for="f-firma">Firma</label><input id="f-firma" name="firma" autocomplete="organization" required></div>
      </div>
      <div class="zwei">
        <div class="feld"><label for="f-kontakt">E-Mail oder Telefon</label><input id="f-kontakt" name="email_oder_telefon" required data-mail-oder-tel></div>
        <div class="feld"><label for="f-anz">Anzahl Fahrzeuge</label><select id="f-anz" name="fahrzeuge" required>
          <option value="" disabled selected>Bitte wählen</option><option>1–4</option><option>5–15</option><option>16–50</option><option>über 50</option>
        </select></div>
      </div>
      <div class="feld"><label for="f-msg">Nachricht <span class="muted">(optional)</span></label><textarea id="f-msg" name="nachricht"></textarea></div>
      <button class="btn btn--primary" type="submit">Kostenlosen Fuhrpark-Check anfragen</button>
      <p class="form-hinweis" aria-live="polite">Ihre Angaben verwenden wir nur zur Bearbeitung Ihrer Anfrage. Mehr in der <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
    </form>
  </div>
</section>
</main>
"""


# ---------------------------------------------------------------- Leistungen
def leistungen_seite():
    details = "\n".join(
        f'''    <article class="detail" id="{a}" data-auf>{icon_box(ic)}<div><h2 style="font-size:1.5rem">{n}</h2><p style="margin-top:.6rem">{t}</p></div><ul>{"".join(f"<li>{icon('check')}<span>{p}</span></li>" for p in punkte)}</ul></article>'''
        for a, ic, n, t, punkte in LEISTUNGEN)
    branchen = "\n".join(f'      <div class="karte" data-auf style="--i:{i}">{icon_box(ic)}<h3>{n}</h3><p>{t}</p></div>' for i, (ic, n, t) in enumerate(BRANCHEN))
    return f"""<main id="top">
{seitenkopf('Leistungen der Fuhrparkverwaltung', 'Neun Bausteine, die Ihnen die Verwaltung Ihres Fuhrparks abnehmen. Alle sind immer enthalten, zum festen Preis pro Fahrzeug.', 'Leistungen')}
<section class="section" style="padding-top:1rem" aria-label="Die neun Leistungsbausteine">
  <div class="container">
{details}
  </div>
</section>
<section class="section section--soft" aria-labelledby="branchen-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf><p class="marke">Für wen</p><h2 id="branchen-titel">Für kleine und mittlere Betriebe</h2><p class="lead">Vor allem für Handwerk, Pflegedienste und Bau mit etwa 5 bis 50 Fahrzeugen.</p></div>
    <div class="karten">
{branchen}
    </div>
  </div>
</section>
{aufruf()}</main>
"""


# ---------------------------------------------------------------- So arbeiten wir
def so_arbeiten_wir_seite():
    schritte = "\n".join(f'      <li class="schritt" data-auf style="--i:{i}"><span class="schritt__nr">{i + 1}</span><h3>{n}</h3><p>{t}</p></li>' for i, (n, t) in enumerate(SCHRITTE))
    preis = "".join(f"<li><span>{n}</span><span>Inklusive</span></li>" for _, _, n, _, _ in LEISTUNGEN)
    return f"""<main id="top">
{seitenkopf('So arbeiten wir', 'In drei Schritten startklar: Erstgespräch, kostenloser Fuhrpark-Check, laufende Betreuung. Danach läuft die Verwaltung Ihres Fuhrparks, ohne dass Sie sich darum kümmern müssen.', 'So arbeiten wir')}
<section class="section" style="padding-top:1rem" aria-label="Die drei Schritte">
  <div class="container"><ol class="schritte">
{schritte}
  </ol></div>
</section>
<section class="section section--soft" id="preis" aria-labelledby="preis-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf><p class="marke">Preis</p><h2 id="preis-titel">Ein Preis pro Fahrzeug</h2><p class="lead">Alle neun Leistungsbausteine sind immer enthalten. Ohne Einzelbuchung, ohne Aufpreis.</p></div>
    <div class="preis">
      <div class="preis__karte" data-auf>
        <h3>Das ist enthalten</h3>
        <ul>{preis}<li><span>Fester Ansprechpartner</span><span>Inklusive</span></li></ul>
        <p class="muted" style="font-size:.9375rem">Ihr genaues Angebot erhalten Sie nach dem kostenlosen Fuhrpark-Check. Abgerechnet wird monatlich, Laufzeit und Kündigungsfristen regelt Ihr Rahmenvertrag.</p>
      </div>
      <div class="rechner" id="rechner" data-auf style="--i:1">
        <h3>Wie viele Termine hat Ihr Fuhrpark?</h3>
        <div aria-live="polite"><output class="wert" id="r-summe">82</output> <span class="lead">Termine im Jahr</span></div>
        <form onsubmit="return false" style="display:grid;gap:.5rem">
          <div class="regler__kopf"><label for="r-fahrzeuge">Fahrzeuge</label><output id="o-fahrzeuge" for="r-fahrzeuge">10</output></div>
          <input type="range" id="r-fahrzeuge" min="1" max="150" value="10">
          <div class="regler__kopf"><label for="r-fahrer">Fahrer:innen</label><output id="o-fahrer" for="r-fahrer">12</output></div>
          <input type="range" id="r-fahrer" min="1" max="200" value="12">
        </form>
        <p class="muted" style="font-size:.9375rem">Typische Intervalle: HU und AU alle 24 Monate, UVV-Prüfung und Wartung jährlich, zwei Reifenwechsel, Führerscheinkontrolle halbjährlich je Person, monatliche Tankabrechnung, jährlicher Versicherungsvergleich.</p>
        <a class="btn btn--primary" id="r-cta" href="index.html#kontakt">Fuhrpark-Check für 10 Fahrzeuge anfragen</a>
      </div>
    </div>
  </div>
</section>
{aufruf()}</main>
"""


# ---------------------------------------------------------------- Über uns
def ueber_uns_seite():
    werte = [
        ("person", "Persönlich", "Ein fester Ansprechpartner, der Ihren Fuhrpark, Ihre Fahrer und Ihre Fristen kennt."),
        ("auszeichnung", "Fachkundig", "Zertifizierte Fuhrparkverwaltung, die Halterhaftung, Prüfpflichten und Dokumentation kennt."),
        ("schloss", "Sorgfältig mit Daten", "Zwei-Faktor-Anmeldung, verschlüsselte Übertragung, getrennte Ablage je Kunde."),
        ("ort", "Aus der Region", "Sitz in Oberhausen, im Einsatz für Betriebe in Duisburg, im Ruhrgebiet und am Niederrhein."),
    ]
    karten = "\n".join(f'      <div class="karte" data-auf style="--i:{i}">{icon_box(ic)}<h3>{n}</h3><p>{t}</p></div>' for i, (ic, n, t) in enumerate(werte))
    return f"""<main id="top">
{seitenkopf('Über uns', 'Wir nehmen Unternehmen die Verwaltung ihrer Firmenfahrzeuge ab.', 'Über uns')}
<section class="section" style="padding-top:1rem" aria-labelledby="wer-titel">
  <div class="container teilung">
    <div class="teilung__bild" data-auf>{bild('dienstwagen', 'Dunkler Dienstwagen auf einem Parkplatz', 1280, 960)}</div>
    <div data-auf style="--i:1">
      <h2 id="wer-titel">Wer sich um Ihren Fuhrpark kümmert</h2>
      <p class="lead">TT Fuhrparkmanagement übernimmt für Unternehmen die Verwaltung ihrer Firmenfahrzeuge. Geleitet wird das Unternehmen von Tolga Topal, zertifizierter Fuhrparkverwalter.</p>
      <p style="margin-top:1rem;color:var(--ink-2)">Wir kennen die Pflichten, die mit einem Fuhrpark verbunden sind: von der Halterhaftung und der regelmäßigen Führerscheinkontrolle über HU, AU und UVV-Prüfung bis zur sauberen Dokumentation. Wir übernehmen die Aufgaben, die im Alltag schnell liegen bleiben, und sorgen dafür, dass Fristen eingehalten, Unterlagen vollständig und Kosten nachvollziehbar sind.</p>
      <p style="margin-top:1rem;color:var(--ink-2)">Bei uns gibt es keine Hotline und kein Ticketsystem, sondern kurze Wege und direkte Absprachen. So bleibt Ihnen die Zeit für Ihr eigentliches Geschäft.</p>
    </div>
  </div>
</section>
<section class="section section--soft" aria-labelledby="werte-titel">
  <div class="container">
    <div class="section__kopf section__kopf--mitte" data-auf><p class="marke">Wofür wir stehen</p><h2 id="werte-titel">Darauf können Sie sich verlassen</h2></div>
    <div class="werte">
{karten}
    </div>
  </div>
</section>
{aufruf()}</main>
"""


def faq_seite():
    items = faq_liste(FRAGEN)
    return f"""<main id="top">
{seitenkopf('Häufige Fragen zur Fuhrparkverwaltung','Kurze Antworten auf das, was wir am häufigsten gefragt werden. Ihre Frage ist nicht dabei? Rufen Sie uns an.', 'FAQ')}
<section class="section" style="padding-top:1rem" aria-label="Fragen und Antworten">
  <div class="container"><div class="faq">
{items}
  </div></div>
</section>
{aufruf()}</main>
"""


def recht_seite(titel, datei):
    inhalt = (ROOT / "src" / "recht" / datei).read_text(encoding="utf-8")
    return f"""<main id="top">
{seitenkopf(titel, '', titel)}
<section class="section" style="padding-top:1rem">
  <div class="container"><article class="recht">
      {inhalt}
  </article></div>
</section>
</main>
"""


DANKE = f"""<main id="top">
<section class="seitenkopf" style="min-height:50vh">
  <div class="container">
    <h1>Danke für Ihre Anfrage</h1>
    <p class="lead">Ihre Anfrage ist angekommen. Wir melden uns innerhalb eines Werktags bei Ihnen.</p>
    <p>Eilig? Rufen Sie uns an: <a class="link" href="{TEL_LINK}">{TELEFON}</a></p>
    <a class="btn btn--primary" href="index.html" style="margin-top:2rem">Zurück zur Startseite</a>
  </div>
</section>
</main>
"""

NICHT_GEFUNDEN = f"""<main id="top">
<section class="seitenkopf" style="min-height:50vh">
  <div class="container">
    <h1>Diese Seite gibt es nicht</h1>
    <p class="lead">Die Adresse ist falsch oder die Seite wurde verschoben. Von der Startseite aus finden Sie alles Wichtige.</p>
    <div class="hero__aktionen">
      <a class="btn btn--primary" href="index.html">Zur Startseite</a>
      <a class="btn btn--ghost" href="index.html#kontakt">Fuhrpark-Check anfragen</a>
    </div>
  </div>
</section>
</main>
"""

BESCHREIBUNG = "Externes Fuhrparkmanagement für kleine Betriebe in Duisburg, im Ruhrgebiet und am Niederrhein: Wir übernehmen Ihre Fuhrparkverwaltung mit festem Ansprechpartner. Jetzt kostenlosen Fuhrpark-Check anfragen."

# (Datei, Titel, Beschreibung, Inhalt, aktiver Menüpunkt, noindex, in Sitemap, zusätzlicher <head>-Inhalt)
SEITEN = [
    ("index.html", "Fuhrparkverwaltung für kleine Betriebe in Duisburg | TT Fuhrparkmanagement", BESCHREIBUNG, startseite(), "", False, True, ""),
    ("leistungen.html", "Leistungen der Fuhrparkverwaltung | TT Fuhrparkmanagement", "Neun Bausteine in einem Paket: Führerscheinkontrolle, Termine, Dokumente, Werkstatt, Schäden, Versicherungsfristen, Tankkarten, Kosten-Reporting und Firmenwagen-Angebote.", leistungen_seite(), "leistungen.html", False, True, ""),
    ("so-arbeiten-wir.html", "So arbeiten wir: Ablauf und Preis | TT Fuhrparkmanagement", "In drei Schritten zur externen Fuhrparkverwaltung: Erstgespräch, kostenloser Fuhrpark-Check, laufende Betreuung. Ein fester Preis pro Fahrzeug.", so_arbeiten_wir_seite(), "so-arbeiten-wir.html", False, True, ""),
    ("ueber-uns.html", "Über uns | TT Fuhrparkmanagement", "TT Fuhrparkmanagement übernimmt für Betriebe in Duisburg, im Ruhrgebiet und am Niederrhein die Verwaltung ihrer Firmenfahrzeuge, persönlich und fachkundig.", ueber_uns_seite(), "ueber-uns.html", False, True, ""),
    ("faq.html", "Häufige Fragen zur Fuhrparkverwaltung | TT Fuhrparkmanagement", "Was kostet externes Fuhrparkmanagement, bin ich an einen Versicherer gebunden, wie schnell geht der Start? Antworten auf häufige Fragen.", faq_seite(), "faq.html", False, True, ""),
    ("impressum.html", "Impressum | TT Fuhrparkmanagement", "Impressum von TT Fuhrparkmanagement, Oberhausen.", recht_seite("Impressum", "impressum.html"), "", False, True, ""),
    ("datenschutz.html", "Datenschutzerklärung | TT Fuhrparkmanagement", "Datenschutzerklärung von TT Fuhrparkmanagement: Hosting, Kontaktformular, Google Ads und Cookie-Einwilligung.", recht_seite("Datenschutzerklärung", "datenschutz.html"), "", False, True, ""),
    ("agb.html", "AGB | TT Fuhrparkmanagement", "Allgemeine Geschäftsbedingungen von TT Fuhrparkmanagement.", recht_seite("Allgemeine Geschäftsbedingungen", "agb.html"), "", False, True, ""),
    ("danke.html", "Danke für Ihre Anfrage | TT Fuhrparkmanagement", "Ihre Anfrage ist angekommen.", DANKE, "", True, False, CONVERSION),
    ("404.html", "Seite nicht gefunden | TT Fuhrparkmanagement", "Diese Seite gibt es nicht.", NICHT_GEFUNDEN, "", True, False, ""),
]

# Interne Links und Dateien absolut machen, damit auch die 404-Seite unter jeder Adresse funktioniert.
_RELATIV = re.compile(r'(href|src|srcset)="(?!https?:|mailto:|tel:|#|/|data:)')


def absolut(html):
    html = _RELATIV.sub(r'\1="/', html)
    return html.replace('href="/index.html#', 'href="/#').replace('href="/index.html"', 'href="/"').replace('href="/index.html?', 'href="/?')


if __name__ == "__main__":
    heute = date.today().isoformat()
    sitemap = []
    for datei, titel, beschr, inhalt, aktiv, robots, in_sitemap, extra in SEITEN:
        pfad = None if robots else datei
        html = absolut(kopf(titel, beschr, aktiv, robots, pfad, extra) + inhalt + fuss())
        (ROOT / datei).write_text(html, encoding="utf-8")
        if in_sitemap:
            loc = SITE + "/" + ("" if datei == "index.html" else datei)
            sitemap.append(f"  <url><loc>{loc}</loc><lastmod>{heute}</lastmod></url>")
        print("gebaut:", datei)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("gebaut: sitemap.xml, robots.txt")
