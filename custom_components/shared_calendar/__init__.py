"""The Shared Calendar integration."""

import logging
import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.lovelace.const import CONF_RESOURCE_TYPE_WS, CONF_URL
from homeassistant.const import CONF_ID, EVENT_HOMEASSISTANT_STARTED, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

HACS_RESOURCE_URL = (
    "/hacsfiles/Snaker-L/Home-Assistant_shared-calendar/www/shared_calendar/"
    "shared-calendar-card.js"
)
MANUAL_RESOURCE_PATH = "www/shared_calendar/shared-calendar-card.js"
MANUAL_RESOURCE_URL = "/local/shared_calendar/shared-calendar-card.js"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Shared Calendar integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Shared Calendar from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if not await _async_register_lovelace_resource(hass):
        def _handle_start(event):
            hass.async_create_task(_async_register_lovelace_resource(hass))

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _handle_start)

    return True


async def _async_register_lovelace_resource(hass: HomeAssistant) -> bool:
    """Register the Shared Calendar Lovelace resource automatically."""
    lovelace_data = hass.data.get("lovelace")
    if not lovelace_data:
        _LOGGER.debug("Lovelace data is not available yet; skipping resource registration.")
        return False

    if lovelace_data.get("mode") == "yaml":
        _LOGGER.warning(
            "Lovelace is running in YAML mode; automatic Shared Calendar resource "
            "registration is not supported."
        )
        return True

    resource_collection = lovelace_data.get("resources")
    if resource_collection is None:
        _LOGGER.debug("Lovelace resources collection is not available.")
        return False

    resource_url = _get_resource_url(hass)
    if resource_url is None:
        _LOGGER.debug("Shared Calendar resource file not found; cannot register resource.")
        return True

    existing_resource = next(
        (
            item
            for item in resource_collection.async_items()
            if item.get(CONF_URL) == resource_url and item.get("type") == "module"
        ),
        None,
    )

    if existing_resource is not None:
        _LOGGER.debug("Shared Calendar Lovelace resource already registered: %s", resource_url)
        return True

    try:
        await resource_collection.async_create_item(
            {CONF_RESOURCE_TYPE_WS: "module", CONF_URL: resource_url}
        )
        _LOGGER.info("Registered Shared Calendar Lovelace resource: %s", resource_url)
        return True
    except Exception as err:
        _LOGGER.error("Failed to register Shared Calendar Lovelace resource: %s", err)
        return True


async def _async_remove_lovelace_resource(hass: HomeAssistant) -> None:
    """Remove the Shared Calendar Lovelace resource when the integration is removed."""
    lovelace_data = hass.data.get("lovelace")
    if not lovelace_data or lovelace_data.get("mode") == "yaml":
        return

    resource_collection = lovelace_data.get("resources")
    if resource_collection is None:
        return

    resource_url = _get_resource_url(hass)
    if resource_url is None:
        return

    resources_to_remove = [
        item
        for item in resource_collection.async_items()
        if item.get(CONF_URL) == resource_url and item.get("type") == "module"
    ]

    for resource in resources_to_remove:
        resource_id = resource.get(CONF_ID)
        if not resource_id:
            continue
        try:
            await resource_collection.async_delete_item(resource_id)
            _LOGGER.info("Removed Shared Calendar Lovelace resource: %s", resource_url)
        except Exception as err:
            _LOGGER.error("Failed to remove Shared Calendar Lovelace resource: %s", err)


def _get_resource_url(hass: HomeAssistant) -> str | None:
    """Return the correct resource URL for the Shared Calendar card."""
    config_path = hass.config.path("www", "shared_calendar", "shared-calendar-card.js")
    if os.path.exists(config_path):
        return MANUAL_RESOURCE_URL

    return HACS_RESOURCE_URL


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Remove a config entry and cleanup the Lovelace resource."""
    await _async_remove_lovelace_resource(hass)
    return True
