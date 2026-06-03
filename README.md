# Home-Assistant Shared Calendar

> ⚠️ **Dies ist zurzeit noch eine Testversion und nicht vollständig funktionsfähig!**

Ein einfacher lokaler Kalender für Home Assistant als Custom Lovelace Card.

## Features

- 📅 **Lokaler Kalender** – Keine externe URL nötig
- 🎨 **Community Card** – Direkt im Dashboard über Lovelace hinzufügbar
- 🔄 **HACS-Integration** – Automatische Updates über HACS
- 🏠 **Home Assistant native** – Vollständige Integration

## Installation

### via HACS

1. Öffne **HACS** in Home Assistant
2. Klicke **Explore & Download Repositories**
3. Suche nach `shared-calendar`
4. Klicke **Download**
5. Starte Home Assistant neu

### Manuelle Installation

Kopiere `custom_components/shared_calendar` in dein Home Assistant `custom_components` Verzeichnis.

```bash
git clone https://github.com/Snaker-L/Home-Assistant_shared-calendar.git
cp -r Home-Assistant_shared-calendar/custom_components/shared_calendar ~/.homeassistant/custom_components/
cp -r Home-Assistant_shared-calendar/www/shared_calendar ~/.homeassistant/www/
```

Starte Home Assistant neu.

## Nutzung

### 1. Integration einrichten

- Gehe zu **Einstellungen → Geräte & Dienste → Integrationen**
- Klicke **+ Integration erstellen**
- Suche nach `Shared Calendar`
- Bestätige die Einrichtung

### 2. Ressource hinzufügen

- Bei HACS-Installation wird die Lovelace-Ressource automatisch registriert.
- Bei manueller Installation kopiere `www/shared_calendar` in dein Home Assistant-Ordner `www/shared_calendar` und starte Home Assistant neu.
- Die Karte sollte danach automatisch im Kartenpicker verfügbar sein.

### 3. Karte zum Dashboard hinzufügen

- Öffne dein Dashboard im Edit-Modus
- Klicke **+ Karte erstellen**
- Wähle unter **Community Cards** → `Shared Calendar Card`
- Konfiguriere die Karte:

```yaml
type: custom:shared-calendar-card
calendar_entity: calendar.family_calendar
title: Familienkalender
days: 14
max_events: 8
```

## Konfiguration

| Option | Beschreibung | Standard |
|--------|-------------|---------|
| `calendar_entity` | Home Assistant Kalender Entity | erforderlich |
| `title` | Titel der Karte | "Shared Calendar" |
| `days` | Anzahl Tage anzeigen | 7 |
| `max_events` | Max. Anzahl Events | 10 |

## Versionshistorie

- **1.0.0** (Testversion) – Erste Release mit Basis-Funktionalität

## Support

Fehler? → [GitHub Issues](https://github.com/Snaker-L/Home-Assistant_shared-calendar/issues)

---

*Made with ❤️ for Home Assistant*
