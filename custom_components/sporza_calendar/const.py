"""Constants for sporza_calendar."""

from logging import Logger, getLogger

from .models import CyclingGame, FormulaOneGame, Game, SoccerGame, TennisGame

LOGGER: Logger = getLogger(__package__)

DOMAIN = "sporza_calendar"
ATTRIBUTION = "Data provided by https://sporza.be/"

GAME_ENDPOINTS = {
    "basketbal": "/web/content/generic/matches/",
    "wielrennen": "/web/content/cycling/matches/",
    "formule1": "/web/content/generic/matches/",
    "tennis": "/web/content/tennis/matches/",
    "voetbal": "/web/content/soccer/matches/",
}

## Basketball and Tennis are not yet implemented
# They are not available in the API, but can be added later if needed.
LABEL_OBJECT_MAPPING = {
    "basketbal": Game,
    "wielrennen": CyclingGame,
    "formule1": FormulaOneGame,
    "tennis": TennisGame,
    "voetbal": SoccerGame,
}

INTERESTED_LABELS = {
    "basketbal",
    "wielrennen",
    "formule1",
    "voetbal",
    "tennis",
}
