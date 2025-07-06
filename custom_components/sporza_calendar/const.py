"""Constants for sporza_calendar."""

from .models import CyclingGame, FormulaOneGame, Game, SoccerGame, TennisGame

DOMAIN = "sporza_calendar"
ATTRIBUTION = "Data provided by https://sporza.be/"

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
