"""Match domain model and selection helpers (test-data layer).

Keeps match parsing and selection out of both the thin API client
and the tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import TypedDict

from utils.outcomes import Outcome


class MatchData(TypedDict):
    """Shape of a single match object from ``GET /api/matches``."""

    id: str
    competition: str
    kickoffDate: str  # YYYY-MM-DD
    homeTeam: str
    awayTeam: str
    odds: dict[str, float]


@dataclass(frozen=True)
class Match:
    """A single match from ``GET /api/matches`` (odds parsed as Decimal)."""

    id: str
    competition: str
    kickoff_date: str  # YYYY-MM-DD
    home_team: str
    away_team: str
    odds: dict[str, Decimal]

    @classmethod
    def from_api(cls, data: MatchData) -> Match:
        return cls(
            id=data["id"],
            competition=data["competition"],
            kickoff_date=data["kickoffDate"],
            home_team=data["homeTeam"],
            away_team=data["awayTeam"],
            odds={k: Decimal(str(v)) for k, v in data["odds"].items()},
        )

    def odds_for(self, outcome: str | Outcome) -> Decimal:
        return self.odds[Outcome(outcome).key]

    @property
    def teams_label(self) -> str:
        return f"{self.home_team} vs {self.away_team}"


def earliest_upcoming_match(matches: list[Match], today: str | None = None) -> Match:
    today = today or date.today().isoformat()
    upcoming = sorted(
        (m for m in matches if m.kickoff_date >= today),
        key=lambda m: m.kickoff_date,
    )
    if not upcoming:
        raise ValueError("no upcoming matches available in the catalogue")
    return upcoming[0]
