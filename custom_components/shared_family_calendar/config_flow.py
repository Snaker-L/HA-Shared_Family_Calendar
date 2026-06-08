"""Config flow for Shared Family Calendar."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_NAME, DOMAIN


class SharedFamilyCalendarConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Shared Family Calendar."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle initial setup."""

        if user_input is not None:
            title = user_input.get(CONF_NAME, DEFAULT_NAME)

            return self.async_create_entry(
                title=title,
                data={
                    CONF_NAME: title,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_NAME,
                        default=DEFAULT_NAME,
                    ): str,
                }
            ),
        )
