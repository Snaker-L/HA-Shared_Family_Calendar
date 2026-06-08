# Shared Family Calendar

> ⚠️ **Aktuell befindet sich die Integration noch in Entwicklung.**

Shared Family Calendar ist eine lokale Kalenderintegration für Home Assistant mit eigener Lovelace-Karte für Familien-, Team- oder Haushaltskalender.

## Features

* 📅 Lokaler Kalender ohne externe ICS-URL
* 👨‍👩‍👧‍👦 Gemeinsamer Familienkalender
* 🎨 Eigene Lovelace Community Card
* 🔄 HACS-Unterstützung
* 🏠 Vollständig lokal in Home Assistant
* ⚡ Automatische Registrierung der Lovelace-Ressource

## Installation

### Installation über HACS

1. Öffne **HACS**
2. Klicke auf **Repositories**
3. Suche nach **Shared Family Calendar**
4. Installiere die Integration
5. Starte Home Assistant neu

### Manuelle Installation

Kopiere den Ordner:

```text
custom_components/shared_family_calendar
```

in dein Home Assistant Verzeichnis:

```text
config/custom_components/shared_family_calendar
```

Anschließend Home Assistant neu starten.

## Einrichtung

### Integration hinzufügen

1. Einstellungen → Geräte & Dienste
2. Integration hinzufügen
3. Nach **Shared Family Calendar** suchen
4. Einrichtung abschließen

## Dashboard-Karte

Nach der Installation steht die Community-Karte automatisch zur Verfügung.

Beispiel:

```yaml
type: custom:shared-family-calendar-card
title: Familienkalender
calendar_entity: calendar.shared_family_calendar
```

## Konfiguration

| Option          | Beschreibung    |
| --------------- | --------------- |
| calendar_entity | Kalender-Entity |
| title           | Titel der Karte |

## Projektstatus

Der Shared Family Calendar befindet sich aktuell noch in aktiver Entwicklung. Funktionen und Datenstruktur können sich bis zur ersten stabilen Version noch ändern.

## Support

Fehler und Verbesserungsvorschläge:

https://github.com/Snaker-L/HA-Shared_Family_Calendar/issues

---

Made with ❤️ for Home Assistant
