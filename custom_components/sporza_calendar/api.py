"""Sporza API Client."""

import json
import logging
from datetime import date, datetime, timedelta

import aiohttp
from homeassistant.util import dt as dt_util

from .const import GAME_ENDPOINTS, INTERESTED_LABELS

_LOGGER = logging.getLogger(__name__)

class SporzaApiClient:
    """Sporza API Client."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the Sporza API Client."""
        self._session = session

    async def async_fetch_games_coming_week(self) -> dict:
        """Get games for the coming week."""
        today = dt_util.now().date()
        week_dates = [today + timedelta(days=i) for i in range(7)]

        week_games = {}
        for day in week_dates:
            games = await self.async_fetch_games_by_day(day)
            week_games[day] = games

        return week_games

    async def async_fetch_games_by_day(self, day: date | None) -> dict:
        """Get games for a specific day from the Sporza API."""
        if day is None:
            day = dt_util.now().date()

        params = {}

        if isinstance(day, (date, datetime)):
            params["date"] = day.strftime("%Y-%m-%d")
        else:
            err = "date must be a datetime.date or datetime.datetime object"
            raise TypeError(err)

        url = "https://api.sporza.be/web/content/schedule"
        async with self._session.get(url, params=params) as response:
            response.raise_for_status()
            text = await response.text()
            data = json.loads(text)
            return self.__parse_schedule(data)

    async def async_fetch_game_metadata_by_id(self, match_id: str, sport: str) -> dict:
        """Get game metadata by match ID from the Sporza API."""
        if sport not in GAME_ENDPOINTS:
            error = f"Unsupported sport: {sport}"
            raise ValueError(error)

        url = f"https://api.sporza.be/{GAME_ENDPOINTS[sport]}{match_id}"

        async with self._session.get(url) as response:
            response.raise_for_status()
            return (await response.json()).get("componentProps", {})

    def __parse_schedule(self, data: dict) -> dict:
        """
        Get the match IDs for interested sports from the schedule data.

        Returns a dictionary with sport labels as keys and lists of match IDs as values.
        """
        matchids_by_sport = {}
        for item in data["componentProps"]["data"]:
            label = item.get("label", "").lower()
            if label in INTERESTED_LABELS:
                matchids = []
                for subitem in item.get("items", []):
                    component = subitem.get("componentProps") or {}
                    match_id = component.get("matchId")
                    if match_id:
                        matchids.append(match_id)
                matchids_by_sport[label] = matchids

        return matchids_by_sport
