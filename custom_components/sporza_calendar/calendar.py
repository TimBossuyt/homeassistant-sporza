"""
Calendar entity for Sporza Calendar integration.

For more details about this integration, please refer to
https://github.com/TimBossuyt/homeassistant-sporza
"""

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import SporzaCalendarDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sporza Calendar."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([SporzaCalendar(coordinator)], update_before_add=True)


class SporzaCalendar(CoordinatorEntity, CalendarEntity):
    """Representation of a Sporza Calendar."""

    def __init__(self, coordinator: SporzaCalendarDataUpdateCoordinator) -> None:
        """Initialize the calendar."""
        super().__init__(coordinator)
        self._attr_name = "Sporza Calendar"
        self._attr_unique_id = f"{DOMAIN}_calendar"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the current or next upcoming event."""
        events = self._get_upcoming_events()
        if events:
            return events[0]
        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,  # noqa: ARG002
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        return self._get_events_in_range(start_date, end_date)

    def _get_upcoming_events(self) -> list[CalendarEvent]:
        """Get upcoming events for the next 7 days."""
        now = dt_util.now()
        end_date = now + timedelta(days=7)
        return self._get_events_in_range(now, end_date)

    def _get_events_in_range(
        self, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get events within a specific date range."""
        events = []

        if not self.coordinator.data:
            return events

        # Coordinator data: {date_key: [game_objects]}
        for date_key, game_objects in self.coordinator.data.items():
            # Convert date_key to datetime for comparison
            if isinstance(date_key, str):
                try:
                    event_date = datetime.fromisoformat(date_key)
                except ValueError:
                    continue
            else:
                event_date = datetime.combine(date_key, datetime.min.time())

            # Set timezone to UTC if not already set
            if event_date.tzinfo is None:
                event_date = event_date.replace(tzinfo=dt_util.UTC)

            # Only include events within our date range
            # (Should be always true as the API takes care of this)
            if start_date.date() <= event_date.date() <= end_date.date():
                for game in game_objects:
                    # Create a unique UUID
                    event_date_str = event_date.strftime("%Y-%m-%d")
                    unique_id = f"sporza_{game.sport}_{game.match_id}_{event_date_str}"

                    start_time = datetime.combine(
                        event_date, game.start_time, tzinfo=ZoneInfo("Europe/Brussels")
                    )
                    end_time = datetime.combine(
                        event_date, game.end_time, tzinfo=ZoneInfo("Europe/Brussels")
                    )

                    # Create a calendar event for each match
                    event = CalendarEvent(
                        start=start_time,
                        end=end_time,
                        summary=game.name,
                        description=game.description,
                        uid=unique_id,
                    )
                    events.append(event)

        # Sort events by start time
        events.sort(key=lambda x: x.start)
        return events

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success
