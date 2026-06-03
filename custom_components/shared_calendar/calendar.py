from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import CONF_ICS_URL, DEFAULT_REFRESH_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    async_add_entities(
        [
            SharedCalendar(
                hass,
                entry.data.get(CONF_NAME, "Shared Calendar"),
                entry.data[CONF_ICS_URL],
            )
        ]
    )


class SharedCalendar(CalendarEntity):

    def __init__(self, hass: HomeAssistant, name: str, ics_url: str) -> None:
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"shared_calendar_{name.lower().replace(' ', '_')}"
        self._ics_url = ics_url
        self._events: list[CalendarEvent] = []
        self._last_update: datetime | None = None

    async def async_get_events(self, hass: HomeAssistant, start_date, end_date):
        if self._last_update is None or dt_util.utcnow() - self._last_update > DEFAULT_REFRESH_INTERVAL:
            await self.async_update()

        return [
            event
            for event in self._events
            if event.start >= start_date and event.end <= end_date
        ]

    async def async_update(self):
        self._events = []

        try:
            session = async_get_clientsession(self.hass)
            response = await session.get(self._ics_url)
            response.raise_for_status()
            content = await response.text()
            self._events = _parse_ics_calendar(content)
            self._last_update = dt_util.utcnow()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.warning("Unable to update shared calendar from %s: %s", self._ics_url, err)
            self._events = []


def _unfold_ics_lines(raw_text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in raw_text.splitlines():
        if raw_line.startswith((" ", "\t")) and lines:
            lines[-1] += raw_line[1:]
        elif raw_line:
            lines.append(raw_line)
    return lines


def _parse_ics_datetime(value: str) -> datetime | None:
    if not value:
        return None

    try:
        dt = dt_util.parse_datetime(value)
    except Exception:
        return None

    if dt is None:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE)

    return dt_util.as_utc(dt)


def _parse_duration(duration: str, start: datetime) -> datetime:
    if duration.startswith("PT"):
        hours = 0
        minutes = 0
        if "H" in duration:
            hours = int(duration.split("PT")[1].split("H")[0])
        if "M" in duration:
            minutes = int(duration.split("H")[-1].split("M")[0])
        return start + timedelta(hours=hours, minutes=minutes)

    return start + timedelta(hours=1)


def _parse_ics_calendar(raw_text: str) -> list[CalendarEvent]:
    lines = _unfold_ics_lines(raw_text)
    events: list[CalendarEvent] = []
    event_data: dict[str, str] = {}
    in_event = False

    for line in lines:
        if line == "BEGIN:VEVENT":
            event_data = {}
            in_event = True
            continue

        if line == "END:VEVENT" and in_event:
            start = _parse_ics_datetime(event_data.get("DTSTART", ""))
            end = _parse_ics_datetime(event_data.get("DTEND", ""))
            if start is None:
                in_event = False
                continue

            if end is None:
                if event_data.get("DURATION"):
                    end = _parse_duration(event_data["DURATION"], start)
                else:
                    end = start + timedelta(hours=1)

            events.append(
                CalendarEvent(
                    start=start,
                    end=end,
                    summary=event_data.get("SUMMARY", "Shared Calendar Event"),
                    description=event_data.get("DESCRIPTION", ""),
                    location=event_data.get("LOCATION", ""),
                    uid=event_data.get("UID"),
                )
            )
            in_event = False
            continue

        if in_event and ":" in line:
            key, value = line.split(":", 1)
            key = key.split(";", 1)[0]
            event_data[key] = value

    return events
