"""
Coordinator for Sporza Calendar integration.

For more details about this integration, please refer to
https://github.com/TimBossuyt/homeassistant-sporza
"""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import SporzaApiClient

_LOGGER = logging.getLogger(__name__)


class SporzaCalendarDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Sporza API."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        sporza_api: SporzaApiClient,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Sporza Calendar",
            config_entry=config_entry,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self.sporza_api = sporza_api

    async def _async_update_data(self) -> dict:
        """Update data via the Sporza API client."""
        try:
            _LOGGER.info("Fetching games for the coming week from Sporza API")
            data = await self.sporza_api.async_fetch_games_coming_week()
        except Exception as exception:
            _LOGGER.exception("Error fetching data from Sporza API")
            message = f"Error fetching data from Sporza API: {exception}"
            raise UpdateFailed(message) from exception
        else:
            return data
