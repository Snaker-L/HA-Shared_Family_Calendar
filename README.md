# Home-Assistant_shared-calendar

A simple Home Assistant custom calendar integration with UI setup and ICS import.

## Installation

1. Kopiere `custom_components/shared_calendar` in dein Home Assistant `custom_components`-Verzeichnis.
2. Starte Home Assistant neu.
3. Öffne Einstellungen -> Geräte & Dienste -> Integration hinzufügen.
4. Suche nach `Shared Calendar` und trage die öffentliche ICS-URL deines Kalenders ein.

## Nutzung

Nach der Integration erscheint im Home Assistant eine Kalender-Entität.

### Community-Karte nutzen

1. Installiere das Repository via HACS oder kopiere es nach `custom_components/shared_calendar`.
2. Starte Home Assistant neu.
3. Füge die Ressource hinzu:
   - Gehe zu `Einstellungen -> Dashboards -> Ressourcen`.
   - Klicke auf `Ressource hinzufügen`.
   - Trage als URL ein: `/local/shared_calendar/shared-calendar-card.js`
   - Typ: `module`
4. Öffne dein Dashboard und füge eine neue Karte hinzu.
5. Suche nach `Shared Calendar Card` oder `custom:shared-calendar-card`.

### Beispielkarte

```yaml
type: custom:shared-calendar-card
calendar_entity: calendar.family_calendar
title: Familienkalender
days: 14
max_events: 8
```

Die Karte kann dann über den Lovelace-Editor konfiguriert werden, ohne dass du komplexe YAML-Strukturen selbst schreiben musst.
