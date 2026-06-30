from __future__ import annotations

from enum import StrEnum


class Endpoint(StrEnum):
    MATCHES = "/matches"
    BALANCE = "/balance"
    PLACE_BET = "/place-bet"
    RESET_BALANCE = "/reset-balance"
