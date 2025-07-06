"""Defines the data model for the different sport games."""

import logging
from datetime import time
from zoneinfo import ZoneInfo

## REMARK: All time attributes should be have timezone Europe/Brussels
## This is the timezone used by Sporza for all game times.

_LOGGER = logging.getLogger(__name__)


class Game:
    """Class representing a generic game."""

    def __init__(self, match_id: str, sport: str, metadata: dict | None = None) -> None:
        """Initialize the game with its attributes."""
        self.match_id = match_id
        self.sport = sport
        self.metadata = metadata or {}

    ## Default properties for all games
    @property
    def start_time(self) -> time:
        """Return the start time of the game."""
        return time(14, 0, tzinfo=ZoneInfo("Europe/Brussels"))

    @property
    def end_time(self) -> time:
        """Return the end time of the game."""
        return time(16, 0, tzinfo=ZoneInfo("Europe/Brussels"))

    @property
    def name(self) -> str:
        """Return the name of the game."""
        return f"{self.sport.capitalize()} Match (ID: {self.match_id})"

    @property
    def description(self) -> str:
        """Return a formatted description of the game."""
        return "Generic Game Description (no specific details available)."

    def __repr__(self) -> str:
        """Return a string representation of the game."""
        return f"Game(match_id={self.match_id}, sport={self.sport})"


class CyclingGame(Game):
    """Class representing a cycling game."""

    def __init__(self, match_id: str, metadata: dict) -> None:
        """Initialize the cycling game with its specific attributes."""
        super().__init__(match_id, "wielrennen", metadata)
        self.stage_name = metadata.get("stage", "")
        self.competition_name = metadata.get("competitionName", "")
        self.game_type = metadata.get("type", "")
        self.url = metadata.get("url", "")

        self.start_label = metadata.get("startLabel", "")
        self.end_label = metadata.get("endLabel", "")

    @property
    def start_time(self) -> time:
        """Return the start time of the Cycling game."""
        time_part = self.start_label.split(" ", 1)[0]
        if time_part:
            try:
                hour, minute = map(int, time_part.split(":"))
                return time(hour, minute, tzinfo=ZoneInfo("Europe/Brussels"))
            except ValueError:
                pass
        return super().start_time

    @property
    def end_time(self) -> time:
        """Return the end time of the Cycling game."""
        time_part = self.end_label.split(" ", 1)[0]
        if time_part:
            try:
                hour, minute = map(int, time_part.split(":"))
                return time(hour, minute, tzinfo=ZoneInfo("Europe/Brussels"))
            except ValueError:
                pass
        return super().end_time

    @property
    def name(self) -> str:
        """Return a concise summary name for calendar display."""
        start_label = self.metadata.get("startLabel", "Onbekend")
        finish_label = self.metadata.get("endLabel", "Onbekend")

        start_location = (
            start_label.split(" ", 1)[1] if " " in start_label else start_label
        )
        finish_location = (
            finish_label.split(" ", 1)[1] if " " in finish_label else finish_label
        )

        return f"🚴‍♂️ {self.competition_name}: {start_location} → {finish_location}"

    @property
    def description(self) -> str:
        """Return a formatted description of the cycling game, with emojis."""
        start_label = self.metadata.get("startLabel", "Onbekend")
        finish_label = self.metadata.get("endLabel", "Onbekend")

        start_location = (
            start_label.split(" ", 1)[1] if " " in start_label else start_label
        )
        finish_location = (
            finish_label.split(" ", 1)[1] if " " in finish_label else finish_label
        )

        return (
            f"🚴‍♂️ {self.competition_name} • {self.game_type}\n"
            f"🏁 Stage: {self.stage_name}\n"
            f"📍 {start_location} → {finish_location}\n"
            f"🔗 Meer info: {self.url or 'Geen URL'}"
        )


class SoccerGame(Game):
    """Class representing a soccer game."""

    def __init__(self, match_id: str, metadata: dict) -> None:
        """Initialize the soccer game with its specific attributes."""
        super().__init__(match_id, "voetbal", metadata)
        self.home_team = metadata["home"]["name"]
        self.away_team = metadata["away"]["name"]
        self.competition_name = metadata.get("competitionName", "")
        self.url = metadata.get("url", "")
        self.meta = metadata.get("meta", "")
        self._start_time = None
        self._end_time = None

        self._parse_times_from_meta()

    @property
    def start_time(self) -> time | None:
        """Return the start time of the soccer game if available."""
        return self._start_time or super().start_time

    @property
    def end_time(self) -> time | None:
        """Return the end time of the soccer game if available."""
        return self._end_time or super().end_time

    @property
    def name(self) -> str:
        """Return a concise summary name for calendar display."""
        return f"⚽️ {self.competition_name}: {self.home_team} vs {self.away_team}"

    @property
    def description(self) -> str:
        """Return a formatted description of the soccer game, with emojis."""
        return (
            f"⚽️ {self.competition_name}\n"
            f"🏟️ {self.home_team} vs {self.away_team}\n"
            f"🔗 Meer info: {self.url or 'Geen URL'}"
        )

    def _parse_times_from_meta(self) -> None:
        """Parse start and end times from metadata."""
        # Example:
        # "meta": "UEFA Champions League - speeldag 1 - 08/07/25 - 18:00"

        try:
            parts = self.meta.split(" - ")
            if len(parts) >= 4:  # noqa: PLR2004
                time_part = parts[3]
                hour, minute = map(int, time_part.split(":"))

        except (ValueError, IndexError):
            error = f"Failed to parse times from meta: {self.meta}. "
            error += "Using default start and end times."
            _LOGGER.warning(error)
            return

        self._start_time = time(hour, minute, tzinfo=ZoneInfo("Europe/Brussels"))
        # Assuming the game lasts 10 minutes for simplicity
        self._end_time = time(hour, minute + 10, tzinfo=ZoneInfo("Europe/Brussels"))


class FormulaOneGame(Game):
    """Class representing a Formula 1 game."""

    def __init__(self, match_id: str, metadata: dict) -> None:
        """Initialize the Formula 1 game with its specific attributes."""
        super().__init__(match_id, "formule1", metadata)
        self.competition_name = metadata.get("competitionName", "")
        self.url = metadata.get("url", "")
        self.rounds = metadata.get("rounds")
        self.location = metadata.get("location", "")
        self.start_label = metadata.get("startLabel", "")
        self.end_label = metadata.get("endLabel", "")

    @property
    def start_time(self) -> time:
        """Return the start time of the Formula 1 game."""
        time_part = self.start_label.split(" ", 1)[0]
        if time_part:
            try:
                hour, minute = map(int, time_part.split(":"))
                return time(hour, minute, tzinfo=ZoneInfo("Europe/Brussels"))
            except ValueError:
                pass
        return super().start_time

    @property
    def end_time(self) -> time:
        """Return the end time of the Formula 1 game."""
        time_part = self.end_label.split(" ", 1)[0]
        if time_part:
            try:
                hour, minute = map(int, time_part.split(":"))
                return time(hour, minute, tzinfo=ZoneInfo("Europe/Brussels"))
            except ValueError:
                pass
        return super().end_time

    @property
    def name(self) -> str:
        """Return a concise summary name for calendar display."""
        return f"🏎️ {self.competition_name} @ {self.location}"

    @property
    def description(self) -> str:
        """Return a formatted description of the Formula 1 game, with emojis."""
        rounds = f"{self.rounds} ronden" if self.rounds else "Onbekend aantal ronden"
        return (
            f"🏁 {self.competition_name}\n"
            f"📍 Locatie: {self.location}\n"
            f"🔄 Ronden: {rounds}\n"
            f"🔗 Meer info: {self.url or 'Geen URL'}"
        )


class TennisGame(Game):
    """Class representing a tennis game."""

    def __init__(self, match_id: str, metadata: dict) -> None:
        """Initialize the tennis game with its specific attributes."""
        super().__init__(match_id, "tennis", metadata)
        self.competition_name = metadata.get("competitionName", "")
        self.home_player = metadata["home"][0]["name"]
        self.away_player = metadata["away"][0]["name"]
        self.url = metadata.get("url", "")
        self.sport = "tennis"

        ## ISSUE: The API does not provide start and end times for tennis games.

    @property
    def name(self) -> str:
        """Return a concise summary name for calendar display."""
        return f"🎾 {self.competition_name}: {self.home_player} vs {self.away_player}"

    @property
    def description(self) -> str:
        """Return a formatted description of the tennis game."""
        return (
            f"🎾 {self.competition_name}:\n"
            f"👤 Spelers: {self.home_player} vs {self.away_player}\n"
            f"🔗 Meer info: {self.url or 'Geen URL'}\n"
        )
