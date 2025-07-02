"""
Calendar entity for Sporza Calendar integration.

For more details about this integration, please refer to
https://github.com/TimBossuyt/homeassistant-sporza
"""

import logging
from datetime import datetime, timedelta

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
        """Return the next upcoming event."""
        events = self._get_upcoming_events()
        if events:
            return events[0]
        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
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
        seen_uids = set()

        if not self.coordinator.data:
            return events

        _LOGGER.debug("Coordinator data: %s", self.coordinator.data)

        # The coordinator data is organized by date -> sport -> list of match IDs
        for date_key, sports_data in self.coordinator.data.items():
            # Convert date_key to datetime for comparison
            if isinstance(date_key, str):
                try:
                    event_date = datetime.fromisoformat(date_key)
                except ValueError:
                    continue
            else:
                event_date = datetime.combine(date_key, datetime.min.time())

            # Make sure the datetime is timezone aware
            if event_date.tzinfo is None:
                event_date = event_date.replace(tzinfo=dt_util.UTC)
            event_date = dt_util.as_local(event_date)

            # Only include events within our date range
            if start_date.date() <= event_date.date() <= end_date.date():
                for sport, match_ids in sports_data.items():
                    if not match_ids:  # Skip if no matches for this sport
                        continue

                    for match_id in match_ids:
                        # Create a more robust UID using the actual date
                        event_date_str = event_date.strftime("%Y-%m-%d")
                        unique_id = f"sporza_{sport}_{match_id}_{event_date_str}"

                        # Skip if we've already seen this UID
                        if unique_id in seen_uids:
                            _LOGGER.debug("Skipping duplicate event: %s", unique_id)
                            continue
                        seen_uids.add(unique_id)

                        # Create a calendar event for each match
                        event = CalendarEvent(
                            start=event_date,
                            end=event_date + timedelta(hours=2),  # 2-hour duration
                            summary=f"{sport.capitalize()} Match",
                            description=f"Sporza {sport} match (ID: {match_id})",
                            uid=unique_id,
                        )
                        events.append(event)
                        _LOGGER.debug("Created event: %s", unique_id)

        # Sort events by start time
        events.sort(key=lambda x: x.start)
        _LOGGER.debug("Total events created: %d", len(events))
        return events

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success
