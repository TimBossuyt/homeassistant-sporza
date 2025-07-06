"""Sporza API Client."""

import json
import logging
from datetime import date, datetime, timedelta

import aiohttp
from homeassistant.util import dt as dt_util

from .const import INTERESTED_LABELS, LABEL_OBJECT_MAPPING
from .models import Game

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
            games_per_sport = await self.async_fetch_games_by_day(day)
            week_games[day] = games_per_sport

        return week_games

    async def async_fetch_games_by_day(self, day: date | None) -> list[Game]:
        """
        Get games for a specific day from the Sporza API.

        Returns a dictionary with sport labels as keys and Game Objects as values.
        """
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

        schedule = self.__parse_schedule(data)

        all_games_for_day = []
        for sport, api_urls in schedule.items():
            for api_url in api_urls:
                game = await self.__async_fetch_game_object_by_id(api_url, sport)
                all_games_for_day.append(game)

        return all_games_for_day

    async def __async_fetch_game_object_by_id(self, api_url: str, sport: str) -> Game:
        """Get game object by match ID."""
        metadata = await self.__async_fetch_game_metadata_by_id(api_url)
        match_id = metadata.get("matchId", 999)

        game_cls = LABEL_OBJECT_MAPPING.get(sport)

        ## Handle generic Game class (as this takes an extra argument)
        if (not game_cls) or (game_cls is Game):
            return Game(
                match_id=match_id,
                sport=sport,
                metadata=metadata,
            )

        return game_cls(match_id=match_id, metadata=metadata)

    async def __async_fetch_game_metadata_by_id(self, api_url: str) -> dict:
        """Get game metadata by match ID from the Sporza API."""
        async with self._session.get(api_url) as response:
            response.raise_for_status()
            text = await response.text()
            data = json.loads(text)
            return data.get("componentProps", {})

    def __parse_schedule(self, data: dict) -> dict:
        """
        Get the match IDs for interested sports from the schedule data.

        Returns a dictionary with sport labels as keys and lists of API urls as values.
        """
        api_urls_by_sport = {}
        for item in data["componentProps"]["data"]:
            label = item.get("label", "").lower()
            if label in INTERESTED_LABELS:
                api_urls = []
                for subitem in item.get("items", []):
                    component = subitem.get("componentProps") or {}
                    api_url = component.get("sportApiUrl")
                    if api_url:
                        api_urls.append(api_url)
                api_urls_by_sport[label] = api_urls

        return api_urls_by_sport
