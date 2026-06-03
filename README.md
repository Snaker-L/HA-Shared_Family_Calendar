# Home-Assistant_shared-calendar

**Das ist zurzeit noch ein Test und nicht funktionsfähig!**

Dies ist ein einfacher lokaler Home Assistant Kalender, der ohne externe ICS-URL arbeitet.

## Nutzung

Der Kalender ist lokal und verwendet eingebaute Termine in Home Assistant.

### Community-Karte

Wenn du das Repository via HACS installierst, wird die Karte automatisch aus dem `www`-Verzeichnis bereitgestellt.

- HACS-Ressource: `/hacsfiles/shared-calendar/shared-calendar-card.js`
- Typ: `module`

Wenn du lokal installierst, kopiere die Datei aus `www/shared-calendar-card.js` in dein Home Assistant `www`-Verzeichnis und verwende dann `/local/shared-calendar-card.js` als Ressource.

Danach kannst du die Karte direkt im Lovelace-Editor auswählen.

### Beispielkarte

```yaml
type: custom:shared-calendar-card
calendar_entity: calendar.family_calendar
title: Familienkalender
days: 14
max_events: 8
```

Die Karte zeigt lokale Kalenderdaten ohne externe URL. Du brauchst keinen zusätzlichen YAML-Code im Dashboard-Editor, sobald die Ressource eingebunden ist.
