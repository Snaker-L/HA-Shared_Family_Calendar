from datetime import datetime, timedelta
from homeassistant.components.calendar import CalendarEntity, CalendarEvent


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([SharedCalendar()], True)


class SharedCalendar(CalendarEntity):

    def __init__(self):
        self._attr_name = "Family Calendar"
        self._attr_unique_id = "family_calendar_1"

    async def async_get_events(self, hass, start_date, end_date):
        return [
            CalendarEvent(
                start=datetime.now(),
                end=datetime.now() + timedelta(hours=1),
                summary="✅ Test Termin",
                description="Shared Calendar läuft!"
            )
        ]

    async def async_update(self):
        return
