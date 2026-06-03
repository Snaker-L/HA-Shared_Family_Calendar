"""The Shared Calendar integration."""

import logging
from pathlib import Path
from shutil import copy2

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.lovelace.const import CONF_RESOURCE_TYPE_WS, CONF_URL
from homeassistant.const import CONF_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

HACS_RESOURCE_URL = (
    "/hacsfiles/Home-Assistant_shared-calendar/www/community/shared_calendar/"
    "shared-calendar-card.js"
)
# Some HACS installations may include the owner in the path; include
# a second variant for cleanup operations.
HACS_RESOURCE_URL_OWNER = (
    "/hacsfiles/Snaker-L/Home-Assistant_shared-calendar/www/community/shared_calendar/"
    "shared-calendar-card.js"
)
MANUAL_RESOURCE_URL = "/local/community/shared_calendar/shared-calendar-card.js"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Shared Calendar integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Shared Calendar from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    if entry.entry_id in hass.data[DOMAIN]:
        _LOGGER.debug("Shared Calendar config entry %s is already set up", entry.entry_id)
        return True
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Ensure the local resource is present for manual installations
    # (creates config/www/community/shared_calendar/shared-calendar-card.js).
    try:
        await _ensure_local_resource(hass)
    except Exception:  # pragma: no cover - defensive
        _LOGGER.debug("Unable to ensure local Shared Calendar resource during setup.")

    if not await _async_register_lovelace_resource(hass):
        def _retry_registration(_: object) -> None:
            _LOGGER.debug("Retrying Shared Calendar Lovelace resource registration.")
            hass.async_create_task(_async_register_lovelace_resource(hass))

        async_call_later(hass, 10, _retry_registration)

    return True


async def _async_register_lovelace_resource(hass: HomeAssistant) -> bool:
    """Register the Shared Calendar Lovelace resource automatically."""
    lovelace_data = hass.data.get("lovelace")
    if not lovelace_data:
        _LOGGER.debug("Lovelace data is not available yet; skipping resource registration.")
        return False
    mode = lovelace_data.get("mode") if isinstance(lovelace_data, dict) else getattr(lovelace_data, "mode", None)
    if mode == "yaml":
        _LOGGER.warning(
            "Lovelace is running in YAML mode; automatic Shared Calendar resource "
            "registration is not supported."
        )
        return True
    resource_collection = lovelace_data.get("resources") if isinstance(lovelace_data, dict) else getattr(lovelace_data, "resources", None)
    if resource_collection is None:
        _LOGGER.debug("Lovelace resources collection is not available.")
        return False

    resource_url = await _get_resource_url(hass)
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
    if not lovelace_data:
        return
    mode = lovelace_data.get("mode") if isinstance(lovelace_data, dict) else getattr(lovelace_data, "mode", None)
    if mode == "yaml":
        return

    resource_collection = lovelace_data.get("resources") if isinstance(lovelace_data, dict) else getattr(lovelace_data, "resources", None)
    if resource_collection is None:
        return

    resource_urls = [MANUAL_RESOURCE_URL, HACS_RESOURCE_URL, HACS_RESOURCE_URL_OWNER]
    resources_to_remove = [
        item
        for item in resource_collection.async_items()
        if item.get(CONF_URL) in resource_urls and item.get("type") == "module"
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


async def _get_resource_url(hass: HomeAssistant) -> str | None:
    """Return the correct resource URL for the Shared Calendar card.

    Prefer the HACS-served resource under `/hacsfiles/...` so the card is
    loaded from the installed HACS package rather than from `/local`.
    """
    # Prefer the HACS resource URL for registration.
    return HACS_RESOURCE_URL


async def _ensure_local_resource(hass: HomeAssistant) -> bool:
    """Ensure the Shared Calendar card file exists under config/www/community/shared_calendar."""
    target_dir = Path(hass.config.path("www", "community", "shared_calendar"))
    target_file = target_dir / "shared-calendar-card.js"

    if target_file.exists():
        return True

    source_file = Path(__file__).resolve().parent / "www" / "shared-calendar-card.js"
    if not source_file.exists():
        _LOGGER.debug("Local Shared Calendar source file not found: %s", source_file)
        return False

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        copy2(source_file, target_file)
        _LOGGER.info("Copied Shared Calendar card to %s", target_file)
        return True
    except OSError as err:
        _LOGGER.error("Unable to copy Shared Calendar card to local www: %s", err)
        return False


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
