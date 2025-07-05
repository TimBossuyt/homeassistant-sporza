"""Constants for sporza_calendar."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "sporza_games"
ATTRIBUTION = "Data provided by https://sporza.be/"

GAME_ENDPOINTS = {
    "basketbal": "/web/content/generic/matches/",
    "wielrennen": "/web/content/cycling/matches/",
    "formule1": "/web/content/generic/matches/",
    "tennis": "/web/content/tennis/matches/",
    "voetbal": "/web/content/soccer/matches/",
}

INTERESTED_LABELS = {
    "basketbal",
    "wielrennen",
    "formule1",
    "voetbal",
    # "tennis",
}
