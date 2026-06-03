# Home-Assistant_shared-calendar

**Das ist zurzeit noch ein Test und nicht funktionsfähig!**

Dies ist ein einfacher lokaler Home Assistant Kalender, der ohne externe ICS-URL arbeitet.

## Nutzung

Der Kalender ist lokal und verwendet eingebaute Termine in Home Assistant.

### Community-Karte

Füge die Karte als HACS-Plugin oder als `custom` Ressource in Home Assistant hinzu.

- URL: `/local/shared_calendar/shared-calendar-card.js`
- Typ: `module`

Danach kannst du die Karte im Lovelace-Editor auswählen.

### Beispielkarte

```yaml
type: custom:shared-calendar-card
calendar_entity: calendar.family_calendar
title: Familienkalender
days: 14
max_events: 8
```

Die Karte zeigt lokale Kalenderdaten ohne externe URL. Du brauchst keinen zusätzlichen YAML-Code im Dashboard-Editor, sobald die Ressource eingebunden ist.
