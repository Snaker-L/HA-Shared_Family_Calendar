"""Calendar entity for Shared Calendar integration."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DEFAULT_NAME

PLATFORMS = ["calendar"]


async def async_setup_entry(
    hass: HomeAssistant, entry: Any, async_add_entities: Any
) -> None:
    """Set up calendar platform for Shared Calendar."""
    calendar_name = entry.data.get(CONF_NAME, DEFAULT_NAME)
    async_add_entities([SharedCalendar(calendar_name)])


class SharedCalendar(CalendarEntity):
    """Shared Calendar entity."""

    def __init__(self, name: str) -> None:
        """Initialize the calendar."""
        self._attr_name = name
        self._attr_unique_id = f"shared_calendar_{name.lower().replace(' ', '_')}"
        self._events: list[CalendarEvent] = []

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Return calendar events within the specified date range."""
        self._events = self._build_sample_events()
        return [
            event
            for event in self._events
            if event.start >= start_date and event.end <= end_date
        ]

    async def async_update(self) -> None:
        """Update calendar events."""
        self._events = self._build_sample_events()

    @staticmethod
    def _build_sample_events() -> list[CalendarEvent]:
        """Build sample calendar events."""
        now = dt_util.now()
        return [
            CalendarEvent(
                start=now,
                end=now + timedelta(hours=1),
                summary="Familien-Meeting",
                description="Lokaler Testtermin im Shared Calendar.",
                location="Zuhause",
                uid="shared-calendar-1",
            ),
            CalendarEvent(
                start=now + timedelta(days=1, hours=2),
                end=now + timedelta(days=1, hours=3),
                summary="Projektplanung",
                description="Lokale Kalenderdaten.",
                location="Büro",
                uid="shared-calendar-2",
            ),
        ]
