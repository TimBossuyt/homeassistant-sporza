"""
Custom integration to integrate the Sporza calendar with Home Assistant.

For more details about this integration, please refer to
https://github.com/TimBossuyt/homeassistant-sporza
"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .api import SporzaApiClient
from .const import DOMAIN
from .coordinator import SporzaCalendarDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["calendar"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # noqa: ARG001
    """Set up the Sporza Calendar integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up sporza_calendar from a config entry."""
    # Store an API client in hass.data for use by the calendar platform
    session = async_get_clientsession(hass)
    api_client = SporzaApiClient(session)

    coordinator = SporzaCalendarDataUpdateCoordinator(
        hass=hass,
        config_entry=entry,
        sporza_api=api_client,
    )

    # Fetch initial data so we have data when entities get added
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up all platforms for this device/entry
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Forward the unloading of the entry to the platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
