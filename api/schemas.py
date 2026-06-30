from __future__ import annotations

from enum import StrEnum

ERROR_ENVELOPE_FIELDS: frozenset[str] = frozenset({"error", "message"})


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
