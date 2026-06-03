import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import CONF_ICS_URL, DEFAULT_NAME, DOMAIN


class SharedCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            title = user_input.get(CONF_NAME) or DEFAULT_NAME
            return self.async_create_entry(title=title, data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_ICS_URL): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
