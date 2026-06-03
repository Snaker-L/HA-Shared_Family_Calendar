from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DEFAULT_NAME


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    async_add_entities(
        [
            SharedCalendar(
                entry.data.get(CONF_NAME, DEFAULT_NAME),
            )
        ]
    )


class SharedCalendar(CalendarEntity):

    def __init__(self, name: str) -> None:
        self._attr_name = name
        self._attr_unique_id = f"shared_calendar_{name.lower().replace(' ', '_')}"
        self._events: list[CalendarEvent] = []

    async def async_get_events(self, hass: HomeAssistant, start_date, end_date):
        self._events = self._build_events()

        return [
            event
            for event in self._events
            if event.start >= start_date and event.end <= end_date
        ]

    async def async_update(self):
        self._events = self._build_events()

    def _build_events(self) -> list[CalendarEvent]:
        now = dt_util.now()
        return [
            CalendarEvent(
                start=now,
                end=now + timedelta(hours=1),
                summary="Familien-Meeting",
                description="Dies ist ein lokaler Testtermin im Shared Calendar.",
                location="Zuhause",
                uid="shared-calendar-1",
            ),
            CalendarEvent(
                start=now + timedelta(days=1, hours=2),
                end=now + timedelta(days=1, hours=3),
                summary="Projektplanung",
                description="Lokale Kalenderdaten ohne externe URL.",
                location="Büro",
                uid="shared-calendar-2",
            ),
        ]
