from __future__ import annotations

from enum import StrEnum

from api.endpoints import Endpoint

ERROR_ENVELOPE_FIELDS: frozenset[str] = frozenset({"error", "message"})

# Single source of truth for each endpoint's *successful* response contract.
# For object endpoints the set is the body's top-level keys (consumed by
# assert_success); for array endpoints (e.g. /matches) it is each item's keys
# (consumed by assert_success_list).
SUCCESS_FIELDS: dict[Endpoint, frozenset[str]] = {
    Endpoint.PLACE_BET: frozenset(
        {"matchId", "selection", "stake", "odds", "payout", "balance", "currency", "message"}
    ),
    Endpoint.BALANCE: frozenset({"balance", "currency"}),
    Endpoint.MATCHES: frozenset({"id", "competition", "homeTeam", "awayTeam", "kickoffDate", "odds"}),
}


class ErrorCode(StrEnum):
    INVALID_STAKE_MIN = ("invalid_stake_min", "Stake must be at least 1.00.")
    INVALID_STAKE_MAX = ("invalid_stake_max", "Stake must be at most 100.00.")
    INVALID_STAKE_PRECISION = ("invalid_stake_precision", "Stake can have up to 2 decimal places.")
    INVALID_STAKE_TYPE = ("invalid_stake_type", "Stake must be a valid number.")

    def __new__(cls, code: str, message: str) -> ErrorCode:
        member = str.__new__(cls, code)
        member._value_ = code
        member.message = message
        return member
